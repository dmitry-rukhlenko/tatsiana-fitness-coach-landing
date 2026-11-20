#!/bin/bash
# One-shot setup for a non-technical collaborator on macOS.
#
# What it does, in order (every step is skipped when already done):
#   1. Git (via Xcode Command Line Tools)
#   2. GitHub CLI `gh` (Homebrew if present, otherwise the official .pkg)
#   3. GitHub login in the browser + git credential helper
#   4. git user.name / user.email (GitHub noreply address, nothing leaks)
#   5. Clone or update the repository into ~/Coding/<repo>
#   6. Check that the collaborator invitation was accepted
#   7. Optional: Node.js + Playwright so `npm test` works
#   8. Open the Claude desktop app (or its download page)
#
# Run:   bash setup-tanya.sh
# Env:   SETUP_DIR=/custom/path   SETUP_NO_OPEN=1   SETUP_NODE=yes|no
#
# Re-running is safe: nothing is reinstalled or overwritten.

set -u

REPO_OWNER="dmitry-rukhlenko"
REPO_NAME="tatsiana-fitness-coach-landing"
REPO="$REPO_OWNER/$REPO_NAME"
TARGET_DIR="${SETUP_DIR:-$HOME/Coding/$REPO_NAME}"
DEFAULT_NAME="Tatsiana Rukhlenko"

ok()   { printf '🟢 %s\n' "$*"; }
info() { printf '🔵 %s\n' "$*"; }
warn() { printf '🟡 %s\n' "$*"; }
fail() { printf '🔴 %s\n' "$*"; }
step() { printf '\n━━━ %s ━━━\n' "$*"; }

die() {
    fail "$*"
    echo
    echo "Скрипт остановлен. Можно исправить причину и запустить его ещё раз:"
    echo "все уже сделанные шаги будут пропущены."
    exit 1
}

if [ "$(uname -s)" != "Darwin" ]; then
    die "Этот скрипт для macOS. Для Windows нужен отдельный скрипт — напиши Дмитрию."
fi

echo "Настройка рабочего места для проекта $REPO_NAME"
echo "Папка проекта: $TARGET_DIR"
echo "Если скрипт спросит пароль — это пароль от этого Mac, он нужен для установки программ."

# ---------------------------------------------------------------- 1. Git
step "1/8 Git"
if xcode-select -p >/dev/null 2>&1 && git --version >/dev/null 2>&1; then
    ok "Git уже установлен: $(git --version)"
else
    warn "Git не найден. Запускаю установку Command Line Tools от Apple."
    xcode-select --install 2>/dev/null || true
    echo
    echo "   Сейчас появится окно macOS с предложением установить инструменты."
    echo "   Нажми «Установить» (Install), дождись окончания (несколько минут),"
    echo "   потом вернись сюда и нажми Enter."
    read -r -p "   Готово? Нажми Enter... " _
    if ! git --version >/dev/null 2>&1; then
        die "Git всё ещё не найден. Заверши установку в окне macOS и запусти скрипт снова."
    fi
    ok "Git установлен: $(git --version)"
fi

# ---------------------------------------------------------------- 2. gh
step "2/8 GitHub CLI (gh)"
if command -v gh >/dev/null 2>&1; then
    ok "gh уже установлен: $(gh --version | head -1)"
elif command -v brew >/dev/null 2>&1; then
    info "Ставлю gh через Homebrew..."
    brew install gh || die "Homebrew не смог установить gh."
    ok "gh установлен: $(gh --version | head -1)"
else
    info "Homebrew нет, скачиваю официальный установщик gh с GitHub..."
    GH_TAG="$(curl -fsSL https://api.github.com/repos/cli/cli/releases/latest \
        | sed -n 's/.*"tag_name": *"v\([^"]*\)".*/\1/p' | head -1)"
    [ -n "$GH_TAG" ] || die "Не удалось узнать версию gh. Проверь интернет и попробуй снова."
    PKG_URL="https://github.com/cli/cli/releases/download/v${GH_TAG}/gh_${GH_TAG}_macOS_universal.pkg"
    PKG_TMP="$(mktemp -d)/gh.pkg"
    curl -fsSL -o "$PKG_TMP" "$PKG_URL" || die "Не удалось скачать $PKG_URL"
    info "Устанавливаю (macOS спросит пароль)..."
    sudo installer -pkg "$PKG_TMP" -target / || die "Установщик gh завершился с ошибкой."
    hash -r
    command -v gh >/dev/null 2>&1 || die "gh установлен, но не виден в PATH. Закрой Терминал, открой заново и запусти скрипт ещё раз."
    ok "gh установлен: $(gh --version | head -1)"
fi

# ---------------------------------------------------------------- 3. login
step "3/8 Вход в GitHub"
if gh auth status --hostname github.com >/dev/null 2>&1; then
    ok "Уже выполнен вход как: $(gh api user --jq .login 2>/dev/null)"
else
    echo "   Сейчас в терминале появится одноразовый код вида XXXX-XXXX и откроется браузер."
    echo "   Войди в GitHub, введи код и нажми Authorize. Потом вернись сюда."
    echo
    gh auth login --hostname github.com --git-protocol https --web \
        || die "Вход не выполнен. Запусти скрипт ещё раз и повтори вход."
    ok "Вход выполнен как: $(gh api user --jq .login)"
fi
gh auth setup-git >/dev/null 2>&1 && ok "git будет использовать вход через gh (пароли вводить не придётся)"

# ---------------------------------------------------------------- 4. git identity
step "4/8 Имя и почта для коммитов"
if [ -z "$(git config --global user.name || true)" ]; then
    read -r -p "   Имя для подписи коммитов [$DEFAULT_NAME]: " NAME_INPUT
    git config --global user.name "${NAME_INPUT:-$DEFAULT_NAME}"
fi
if [ -z "$(git config --global user.email || true)" ]; then
    # GitHub's noreply address: commits are attributed to the account,
    # the real mailbox never appears in the public history.
    NOREPLY="$(gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"' 2>/dev/null)"
    [ -n "$NOREPLY" ] || die "Не удалось получить данные аккаунта GitHub."
    git config --global user.email "$NOREPLY"
fi
git config --global init.defaultBranch main >/dev/null 2>&1 || true
git config --global pull.rebase false >/dev/null 2>&1 || true
ok "Коммиты будут подписаны: $(git config --global user.name) <$(git config --global user.email)>"

# ---------------------------------------------------------------- 5. clone
step "5/8 Проект"
if [ -d "$TARGET_DIR/.git" ]; then
    ok "Проект уже скачан, подтягиваю свежие изменения..."
    (cd "$TARGET_DIR" && git fetch --quiet origin && git status --short --branch | head -1)
elif [ -e "$TARGET_DIR" ]; then
    die "Папка $TARGET_DIR существует, но это не Git-репозиторий. Переименуй или удали её и запусти снова."
else
    mkdir -p "$(dirname "$TARGET_DIR")"
    gh repo clone "$REPO" "$TARGET_DIR" || die "Не удалось скачать репозиторий."
    ok "Проект скачан в $TARGET_DIR"
fi

# ---------------------------------------------------------------- 6. access
step "6/8 Право отправлять изменения"
CAN_PUSH="$(gh api "repos/$REPO" --jq '.permissions.push' 2>/dev/null || echo unknown)"
case "$CAN_PUSH" in
    true)  ok "Доступ на запись есть. Можно отправлять ветки и создавать pull request." ;;
    false)
        warn "Доступа на запись пока нет: приглашение не принято или ещё не отправлено."
        echo "   Открываю страницу приглашений. Если там пусто — попроси Дмитрия пригласить тебя"
        echo "   (ему нужен твой логин: $(gh api user --jq .login 2>/dev/null))."
        [ -z "${SETUP_NO_OPEN:-}" ] && open "https://github.com/$REPO/invitations"
        echo "   Смотреть и править сайт можно уже сейчас; отправка на GitHub заработает после принятия."
        ;;
    *)     warn "Не удалось проверить права (нет сети?). Проверим в следующий раз." ;;
esac

# ---------------------------------------------------------------- 7. node (optional)
step "7/8 Node.js для проверок (необязательно)"
if command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
    ok "Node.js уже есть: $(node --version)"
    WANT_NODE=yes
else
    WANT_NODE="${SETUP_NODE:-}"
    if [ -z "$WANT_NODE" ]; then
        echo "   Node.js нужен только чтобы запускать npm test (автопроверка сайта)."
        echo "   Для правок текста и картинок он не нужен; Дмитрий проверит при приёме."
        read -r -p "   Установить Node.js сейчас? [y/N]: " ANSWER
        case "$ANSWER" in y|Y|yes|да|д) WANT_NODE=yes ;; *) WANT_NODE=no ;; esac
    fi
    if [ "$WANT_NODE" = "yes" ]; then
        if command -v brew >/dev/null 2>&1; then
            brew install node || warn "Homebrew не смог установить Node.js."
        else
            NODE_VER="$(curl -fsSL https://nodejs.org/dist/index.json \
                | sed -n 's/.*"version": *"\(v[^"]*\)".*"lts": *"[A-Z][a-z]*".*/\1/p' | head -1)"
            if [ -n "$NODE_VER" ]; then
                NODE_PKG="$(mktemp -d)/node.pkg"
                curl -fsSL -o "$NODE_PKG" "https://nodejs.org/dist/$NODE_VER/node-$NODE_VER.pkg" \
                    && sudo installer -pkg "$NODE_PKG" -target / \
                    || warn "Установка Node.js не удалась. Можно поставить вручную с https://nodejs.org/"
                hash -r
            else
                warn "Не удалось узнать версию Node.js. Поставь вручную с https://nodejs.org/"
            fi
        fi
    else
        info "Пропускаю Node.js. Его можно поставить позже, запустив скрипт ещё раз."
    fi
fi
if [ "$WANT_NODE" = "yes" ] && command -v npm >/dev/null 2>&1; then
    info "Ставлю зависимости проекта и браузер для тестов (пара минут)..."
    (cd "$TARGET_DIR" && npm install --silent && npx --yes playwright install chromium >/dev/null 2>&1) \
        && ok "npm test готов к запуску" \
        || warn "Зависимости не поставились до конца. Попроси Claude: «запусти npm install и npx playwright install chromium»."
fi

# ---------------------------------------------------------------- 8. Claude
step "8/8 Приложение Claude"
if [ -d "/Applications/Claude.app" ] || [ -d "$HOME/Applications/Claude.app" ]; then
    ok "Приложение Claude установлено."
    [ -z "${SETUP_NO_OPEN:-}" ] && open -a Claude 2>/dev/null
else
    warn "Приложение Claude не найдено. Открываю страницу загрузки: https://claude.ai/download"
    [ -z "${SETUP_NO_OPEN:-}" ] && open "https://claude.ai/download"
fi

# ---------------------------------------------------------------- done
echo
echo "════════════════════════════════════════════════════════════"
echo "🟢 Готово. Что дальше:"
echo
echo "  1. В приложении Claude открой вкладку Code."
echo "  2. Нажми «новая сессия» и выбери папку:"
echo "     $TARGET_DIR"
echo "  3. Напиши Claude первое сообщение, например:"
echo "     «Прочитай ONBOARDING.md и PRODUCT.md и расскажи, как тут принято работать»."
echo
echo "  Главное правило: не править ветку main напрямую — она публикуется на живой сайт."
echo "  Для каждой задачи: новая ветка → правки → pull request. Подробности в ONBOARDING.md."
echo "════════════════════════════════════════════════════════════"
