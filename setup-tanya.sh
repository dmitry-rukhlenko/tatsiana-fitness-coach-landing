#!/bin/bash
# One-shot workstation setup for a non-technical collaborator on macOS.
# Every message is in plain Russian and explains what happens and why.
#
# Steps (each one is skipped when already done, so re-running is safe):
#   1. Git (Apple Command Line Tools)
#   2. GitHub CLI `gh` (Homebrew if present, otherwise the official .pkg)
#   3. GitHub login in the browser + git credential helper
#   4. git user.name / user.email (GitHub noreply address)
#   5. Clone or refresh the repository into ~/Coding/<repo>
#   6. Check that the collaborator invitation was accepted
#   7. Optional: Node.js + Playwright so `npm test` works
#   8. Open the Claude desktop app (or its download page)
#
# Everything printed is also written to ~/Desktop/setup-log.txt so the
# collaborator can send that file when something goes wrong.
#
# Run:   bash setup-tanya.sh
# Env:   SETUP_DIR=/custom/path   SETUP_NO_OPEN=1   SETUP_NODE=yes|no   SETUP_LOG=/custom/log

set -u

REPO_OWNER="dmitry-rukhlenko"
REPO_NAME="tatsiana-fitness-coach-landing"
REPO="$REPO_OWNER/$REPO_NAME"
TARGET_DIR="${SETUP_DIR:-$HOME/Coding/$REPO_NAME}"
DEFAULT_NAME="Tatsiana Rukhlenko"
LOG="${SETUP_LOG:-$HOME/Desktop/setup-log.txt}"
TOTAL=8

# Mirror everything to the log file. Interactive prompts (sudo, gh) talk to
# the terminal directly, so they still work.
mkdir -p "$(dirname "$LOG")"
exec > >(tee -a "$LOG") 2>&1
printf '\n===== Запуск %s =====\n' "$(date '+%Y-%m-%d %H:%M:%S')" >>"$LOG"

ok()   { printf '   🟢 %s\n' "$*"; }
info() { printf '   🔵 %s\n' "$*"; }
warn() { printf '   🟡 %s\n' "$*"; }
fail() { printf '   🔴 %s\n' "$*"; }
say()  { printf '   %s\n' "$*"; }
step() { printf '\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n  Шаг %s из %s: %s\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n' "$1" "$TOTAL" "$2"; }
pause_enter() { printf '\n'; read -r -p "   ▶ Когда будешь готова, нажми Enter... " _ 2>/dev/null </dev/tty || true; printf '\n'; }

die() {
    printf '\n'
    fail "$*"
    printf '\n'
    say "Скрипт остановился. Это не страшно: ничего не сломано."
    say "Что сделать:"
    say "  1. Прочитай сообщение выше — там написано, в чём причина."
    say "  2. Если непонятно, отправь Дмитрию файл setup-log.txt с Рабочего стола."
    say "     Сейчас он откроется в Finder, его можно перетащить в мессенджер."
    say "  3. После исправления запусти ту же строку в Терминале ещё раз:"
    say "     всё, что уже получилось, скрипт пропустит."
    [ -z "${SETUP_NO_OPEN:-}" ] && open -R "$LOG" 2>/dev/null
    exit 1
}

if [ "$(uname -s)" != "Darwin" ]; then
    die "Этот скрипт только для Mac. У тебя другая система — напиши Дмитрию, он пришлёт другой вариант."
fi

clear 2>/dev/null || true
cat <<EOF

  ╔══════════════════════════════════════════════════════════════╗
  ║   Настройка компьютера для работы над сайтом                 ║
  ║   $REPO_NAME                             ║
  ╚══════════════════════════════════════════════════════════════╝

   Привет! Этот помощник подготовит твой Mac, чтобы ты могла править
   сайт вместе с Claude и отправлять изменения Дмитрию.

   Он сделает $TOTAL шагов и перед каждым расскажет, что происходит:

     1. Проверит программу Git (хранит историю изменений файлов).
     2. Поставит GitHub CLI — через неё компьютер «разговаривает» с GitHub.
     3. Войдёт в твой аккаунт GitHub через браузер.
     4. Запишет, каким именем подписывать твои правки.
     5. Скачает сайт в папку  $TARGET_DIR
     6. Проверит, что Дмитрий дал тебе доступ.
     7. Спросит, ставить ли Node.js (нужен только для автопроверок).
     8. Откроет приложение Claude.

   Что может понадобиться от тебя:
     • пароль от этого Mac — когда ставятся программы. При вводе символы
       НЕ видны, это нормально: просто набери пароль и нажми Enter;
     • нажать кнопку в окне macOS или в браузере — скрипт скажет, когда;
     • ответить на один вопрос буквой y или n.

   Всё, что здесь появится, сохраняется в файл setup-log.txt на Рабочем
   столе. Если что-то пойдёт не так — просто отправь этот файл Дмитрию.

   Скрипт можно запускать сколько угодно раз: что уже сделано, он пропустит.
EOF
pause_enter

# ---------------------------------------------------------------- 1. Git
step 1 "Git"
say "Git — это программа, которая запоминает каждое изменение в файлах сайта."
say "Благодаря ей любую правку можно откатить, а два человека не затирают"
say "работу друг друга. Проверяю, установлена ли она..."
printf '\n'
if xcode-select -p >/dev/null 2>&1 && git --version >/dev/null 2>&1; then
    ok "Git уже есть: $(git --version). Ничего делать не нужно."
else
    warn "Git ещё не установлен. Его ставит сама Apple, это бесплатно."
    xcode-select --install 2>/dev/null || true
    printf '\n'
    say "Сейчас на экране появится окно macOS с предложением установить"
    say "«Command Line Tools» (инструменты командной строки)."
    say "  1. Нажми в нём «Установить» (Install) и согласись с условиями."
    say "  2. Подожди, пока установка закончится — обычно 5–10 минут."
    say "  3. Когда окно скажет «Готово», вернись сюда."
    pause_enter
    if ! git --version >/dev/null 2>&1; then
        die "Git всё ещё не найден. Возможно, установка ещё идёт или была отменена. Дождись её окончания и запусти скрипт снова."
    fi
    ok "Git установлен: $(git --version)"
fi

# ---------------------------------------------------------------- 2. gh
step 2 "GitHub CLI"
say "GitHub — это сайт, где хранится общая копия проекта. GitHub CLI (команда gh)"
say "позволяет компьютеру входить в твой аккаунт и скачивать или отправлять файлы."
say "Проверяю..."
printf '\n'
if command -v gh >/dev/null 2>&1; then
    ok "GitHub CLI уже есть: $(gh --version | head -1). Ничего делать не нужно."
elif command -v brew >/dev/null 2>&1; then
    info "У тебя есть Homebrew (менеджер программ для Mac). Ставлю gh через него,"
    info "это займёт около минуты..."
    brew install gh || die "Homebrew не смог установить gh. Проверь интернет и попробуй ещё раз."
    ok "GitHub CLI установлен: $(gh --version | head -1)"
else
    info "Скачиваю официальный установщик gh с сайта GitHub..."
    GH_TAG="$(curl -fsSL https://api.github.com/repos/cli/cli/releases/latest \
        | sed -n 's/.*"tag_name": *"v\([^"]*\)".*/\1/p' | head -1)"
    [ -n "$GH_TAG" ] || die "Не удалось связаться с GitHub. Проверь, что интернет работает, и запусти скрипт снова."
    PKG_URL="https://github.com/cli/cli/releases/download/v${GH_TAG}/gh_${GH_TAG}_macOS_universal.pkg"
    PKG_TMP="$(mktemp -d)/gh.pkg"
    curl -fsSL -o "$PKG_TMP" "$PKG_URL" || die "Не удалось скачать установщик gh. Проверь интернет и попробуй ещё раз."
    ok "Скачано (версия $GH_TAG)."
    printf '\n'
    say "Сейчас установщик попросит ПАРОЛЬ ОТ ЭТОГО MAC — тот, которым ты"
    say "входишь в компьютер. Это нужно, чтобы поставить программу для всех"
    say "пользователей. Символы при вводе не отображаются — набери пароль"
    say "«вслепую» и нажми Enter."
    printf '\n'
    sudo installer -pkg "$PKG_TMP" -target / || die "Установка gh не удалась (возможно, пароль введён неверно). Запусти скрипт ещё раз."
    hash -r
    command -v gh >/dev/null 2>&1 || die "gh установлен, но Терминал его пока не видит. Закрой окно Терминала, открой новое и запусти скрипт ещё раз."
    ok "GitHub CLI установлен: $(gh --version | head -1)"
fi

# ---------------------------------------------------------------- 3. login
step 3 "Вход в GitHub"
say "Теперь компьютеру нужно войти в твой аккаунт GitHub, чтобы он мог"
say "скачивать и отправлять файлы от твоего имени. Делается один раз."
printf '\n'
if gh auth status --hostname github.com >/dev/null 2>&1; then
    ok "Вход уже выполнен. Ты — $(gh api user --jq .login 2>/dev/null). Ничего делать не нужно."
else
    say "Что сейчас произойдёт:"
    say "  1. Ниже появится ОДНОРАЗОВЫЙ КОД вида XXXX-XXXX. Запомни или скопируй его."
    say "  2. Откроется браузер со страницей GitHub (если нет — нажми Enter здесь,"
    say "     и скрипт покажет ссылку, которую нужно открыть)."
    say "  3. Если GitHub попросит — войди со своим логином и паролем GitHub."
    say "  4. Введи код в окошко на странице и нажми Continue, затем Authorize."
    say "  5. Вернись в это окно. Скрипт сам продолжит."
    pause_enter
    gh auth login --hostname github.com --git-protocol https --web \
        || die "Вход в GitHub не завершился. Запусти скрипт ещё раз и повтори шаг — код будет новый."
    ok "Вход выполнен. Ты — $(gh api user --jq .login)."
fi
if gh auth setup-git >/dev/null 2>&1; then
    ok "Git связан с этим входом: пароль больше вводить не придётся."
fi

# ---------------------------------------------------------------- 4. git identity
step 4 "Подпись для правок"
say "Каждое сохранённое изменение (коммит) подписывается именем автора."
say "Так Дмитрий видит, что правка от тебя."
printf '\n'
if [ -z "$(git config --global user.name || true)" ]; then
    say "Как подписывать твои правки? Нажми просто Enter, чтобы оставить"
    say "«$DEFAULT_NAME», или напиши другое имя."
    read -r -p "   Имя [$DEFAULT_NAME]: " NAME_INPUT 2>/dev/null </dev/tty || NAME_INPUT=""
    git config --global user.name "${NAME_INPUT:-$DEFAULT_NAME}"
    ok "Имя записано."
else
    ok "Имя уже задано раньше: $(git config --global user.name)."
fi
if [ -z "$(git config --global user.email || true)" ]; then
    # GitHub's noreply address keeps the real mailbox out of public history.
    NOREPLY="$(gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"' 2>/dev/null)"
    [ -n "$NOREPLY" ] || die "Не удалось получить данные аккаунта GitHub. Проверь интернет и запусти скрипт снова."
    git config --global user.email "$NOREPLY"
    ok "Почта записана: $NOREPLY"
    say "Это служебный адрес GitHub: твоя настоящая почта никуда не публикуется."
else
    ok "Почта уже задана раньше: $(git config --global user.email)."
fi
git config --global init.defaultBranch main >/dev/null 2>&1 || true
git config --global pull.rebase false >/dev/null 2>&1 || true

# ---------------------------------------------------------------- 5. clone
step 5 "Скачиваем сайт"
say "Теперь скачиваю все файлы сайта (это называется «клонировать репозиторий»)"
say "в папку:  $TARGET_DIR"
say "«Coding» — папка внутри твоей домашней папки, она появится сама."
printf '\n'
if [ -d "$TARGET_DIR/.git" ]; then
    ok "Сайт уже скачан. Подтягиваю свежие изменения с GitHub..."
    (cd "$TARGET_DIR" && git fetch --quiet origin) && ok "Готово, копия обновлена."
elif [ -e "$TARGET_DIR" ]; then
    die "Папка $TARGET_DIR уже существует, но это не копия проекта. Переименуй или удали её и запусти скрипт снова."
else
    mkdir -p "$(dirname "$TARGET_DIR")"
    gh repo clone "$REPO" "$TARGET_DIR" -- --quiet || die "Не удалось скачать сайт. Проверь интернет и запусти скрипт снова."
    ok "Сайт скачан. Внутри — $(find "$TARGET_DIR" -type f -not -path '*/.git/*' | wc -l | tr -d ' ') файлов."
fi

# ---------------------------------------------------------------- 6. access
step 6 "Проверяем доступ"
say "Скачать сайт может кто угодно, а вот ОТПРАВЛЯТЬ изменения обратно —"
say "только те, кого Дмитрий пригласил. Проверяю, принято ли приглашение..."
printf '\n'
CAN_PUSH="$(gh api "repos/$REPO" --jq '.permissions.push' 2>/dev/null || echo unknown)"
case "$CAN_PUSH" in
    true)
        ok "Доступ есть. Ты можешь отправлять свои правки на GitHub."
        ;;
    false)
        warn "Доступа пока нет. Это значит одно из двух:"
        say "  • Дмитрий ещё не отправил приглашение — напиши ему свой логин:"
        say "    $(gh api user --jq .login 2>/dev/null)"
        say "  • приглашение отправлено, но не принято — сейчас откроется страница,"
        say "    где его можно принять (кнопка Accept). Если страница пустая,"
        say "    проверь почту: письмо от GitHub со словами «invited you»."
        [ -z "${SETUP_NO_OPEN:-}" ] && open "https://github.com/$REPO/invitations"
        printf '\n'
        say "Это не мешает продолжить: смотреть и править сайт у себя можно уже"
        say "сейчас. Отправка на GitHub заработает, как только приглашение принято."
        ;;
    *)
        warn "Не удалось проверить доступ (похоже, нет связи с GitHub). Проверим в другой раз."
        ;;
esac

# ---------------------------------------------------------------- 7. node (optional)
step 7 "Node.js для автопроверок (по желанию)"
say "В проекте есть автоматическая проверка, что сайт не сломался (команда npm test)."
say "Для неё нужна программа Node.js. Для правок текста и картинок она НЕ нужна:"
say "Дмитрий всё равно проверяет каждое изменение перед публикацией."
printf '\n'
if command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
    ok "Node.js уже есть: $(node --version)."
    WANT_NODE=yes
else
    WANT_NODE="${SETUP_NODE:-}"
    if [ -z "$WANT_NODE" ]; then
        say "Поставить Node.js сейчас? Это ещё 2–5 минут и, возможно, пароль от Mac."
        say "Если сомневаешься — ответь n. Поставить можно будет позже, запустив"
        say "скрипт ещё раз."
        read -r -p "   Ставить Node.js? Напиши y (да) или n (нет) и нажми Enter [n]: " ANSWER 2>/dev/null </dev/tty || ANSWER=""
        case "$ANSWER" in y|Y|yes|да|д|Д) WANT_NODE=yes ;; *) WANT_NODE=no ;; esac
    fi
    if [ "$WANT_NODE" = "yes" ]; then
        if command -v brew >/dev/null 2>&1; then
            info "Ставлю Node.js через Homebrew..."
            brew install node || warn "Homebrew не смог установить Node.js. Пропускаю."
        else
            info "Узнаю актуальную стабильную версию Node.js..."
            NODE_VER="$(curl -fsSL https://nodejs.org/dist/index.json \
                | sed -n 's/.*"version": *"\(v[^"]*\)".*"lts": *"[A-Z][a-z]*".*/\1/p' | head -1)"
            if [ -n "$NODE_VER" ]; then
                NODE_PKG="$(mktemp -d)/node.pkg"
                info "Скачиваю Node.js $NODE_VER..."
                if curl -fsSL -o "$NODE_PKG" "https://nodejs.org/dist/$NODE_VER/node-$NODE_VER.pkg"; then
                    say "Установщик снова попросит пароль от Mac (символы не видны — это нормально)."
                    sudo installer -pkg "$NODE_PKG" -target / \
                        || warn "Установка Node.js не удалась. Можно поставить позже вручную с https://nodejs.org/"
                    hash -r
                else
                    warn "Не удалось скачать Node.js. Пропускаю."
                fi
            else
                warn "Не удалось узнать версию Node.js. Пропускаю."
            fi
        fi
    else
        info "Хорошо, пропускаю Node.js."
    fi
fi
if [ "$WANT_NODE" = "yes" ] && command -v npm >/dev/null 2>&1; then
    info "Ставлю вспомогательные файлы для проверки и браузер для тестов."
    info "Это 1–3 минуты, на экране может ничего не меняться — это нормально..."
    if (cd "$TARGET_DIR" && npm install --silent && npx --yes playwright install chromium >/dev/null 2>&1); then
        ok "Автопроверка готова. Позже можно сказать Claude: «запусти npm test»."
    else
        warn "Не всё поставилось. Не страшно: позже попроси Claude «запусти npm install и npx playwright install chromium»."
    fi
fi

# ---------------------------------------------------------------- 8. Claude
step 8 "Приложение Claude"
say "Claude Code — часть приложения Claude, где ты пишешь задачи обычными"
say "словами, а Claude сам правит файлы сайта. Проверяю, установлено ли оно..."
printf '\n'
if [ -d "/Applications/Claude.app" ] || [ -d "$HOME/Applications/Claude.app" ]; then
    ok "Приложение Claude установлено. Открываю его."
    [ -z "${SETUP_NO_OPEN:-}" ] && open -a Claude 2>/dev/null
else
    warn "Приложение Claude не найдено. Открываю страницу, откуда его скачать:"
    say "https://claude.ai/download  — скачай, перетащи в «Программы», открой и войди."
    [ -z "${SETUP_NO_OPEN:-}" ] && open "https://claude.ai/download"
fi

# ---------------------------------------------------------------- done
cat <<EOF


  ╔══════════════════════════════════════════════════════════════╗
  ║   🟢 Всё готово!                                             ║
  ╚══════════════════════════════════════════════════════════════╝

   Файлы сайта лежат здесь:
     $TARGET_DIR

   Что делать дальше:

     1. В приложении Claude открой вкладку «Code».
     2. Claude предложит выбрать папку проекта — выбери папку
        «$REPO_NAME» внутри «Coding».
        (Сейчас эта папка откроется в Finder, чтобы было видно, где она.)
     3. Напиши Claude первое сообщение, например:

        «Прочитай ONBOARDING.md и расскажи, как тут принято работать»

   Самое важное правило: не менять ветку main напрямую — она публикуется
   на живой сайт. Для каждой задачи: новая ветка → правки → pull request.
   Подробно это объяснено в файле ONBOARDING.md, и Claude его знает.

   Этот Терминал можно закрыть.

EOF
[ -z "${SETUP_NO_OPEN:-}" ] && open "$TARGET_DIR" 2>/dev/null
sleep 0.3
exit 0
