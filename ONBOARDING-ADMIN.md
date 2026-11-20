# Подключение соавтора: шпаргалка для владельца репозитория

Пара к `ONBOARDING.md` (инструкция для Тани) и `setup-tanya.sh` (скрипт
настройки её Mac). Здесь то, что делаешь ты.

## 1. Порядок действий

1. **Запушить `main`** с файлами `ONBOARDING.md`, `ONBOARDING-ADMIN.md` и
   `setup-tanya.sh`. Таня скачивает скрипт по raw-ссылке из `main`, поэтому
   до пуша строка из её инструкции не сработает.
2. **Защитить `main`** (пункт 3 ниже). Лучше до того, как у Тани появится
   доступ.
3. **Отправить Тане сообщение** (пункт 2) и дождаться её логина GitHub.
4. **Пригласить её** в репозиторий (пункт 4).
5. Дальше она идёт по `ONBOARDING.md` сама. Если скрипт у неё упадёт, она
   пришлёт `setup-log.txt` с Рабочего стола: там весь вывод с датой запуска.

Архив с файлами посылать не нужно: ей достаточно одной строки в Терминале,
она скачивает скрипт сама. «Распаковать и выполнить инструкцию через Claude»
тоже не нужно: скрипт задуман так, чтобы Claude на этом этапе ещё не
требовался (у неё его может и не быть), а интерактивные шаги — пароль Mac,
код в браузере — удобнее проходить в обычном Терминале.

## 2. Текст сообщения для Тани

Можно отправить как есть.

```text
Таня, привет! Чтобы ты могла править сайт вместе с Claude, нужно один раз
настроить компьютер. Я подготовил инструкцию, где всё расписано для
человека без опыта программирования:

https://github.com/dmitry-rukhlenko/tatsiana-fitness-coach-landing/blob/main/ONBOARDING.md

Коротко:
1. Заведи аккаунт на https://github.com/signup и пришли мне свой логин —
   я добавлю тебя в проект, тебе придёт письмо «invited you to collaborate»,
   нажми там Accept.
2. Установи приложение Claude: https://claude.ai/download
3. Открой на Mac программу «Терминал» (Cmd+пробел, набери Терминал), вставь
   туда эту строку целиком и нажми Enter:

curl -fsSL https://raw.githubusercontent.com/dmitry-rukhlenko/tatsiana-fitness-coach-landing/main/setup-tanya.sh -o ~/Downloads/setup-tanya.sh && bash ~/Downloads/setup-tanya.sh

Дальше скрипт сам всё установит и по-русски объяснит каждый шаг. Он может
попросить пароль от Mac (при вводе символы не видны, это нормально) и
ввести код на сайте GitHub. Если что-то пойдёт не так, на Рабочем столе
появится файл setup-log.txt — просто пришли его мне.
```

## 3. Защитить `main`

GitHub Pages публикует сайт из ветки `main`, папка `/`. На 20 ноября 2026
ветка не защищена: любой соавтор может запушить в неё напрямую, и правка
через минуту окажется на живом сайте. Инструкция велит Тане работать через
ветки и pull request, но надёжнее, чтобы это обеспечивал GitHub.

1. Открой <https://github.com/dmitry-rukhlenko/tatsiana-fitness-coach-landing/settings/rules>
2. **New ruleset** → **New branch ruleset**.
3. Ruleset Name: `protect-main`. Enforcement status: **Active**.
4. Bypass list → **Add bypass** → **Repository admin**. Это ты: сможешь
   коммитить в `main` напрямую, когда работаешь один.
5. Target branches → **Add target** → **Include default branch**.
6. В разделе Rules включить:
   - **Restrict deletions**
   - **Block force pushes**
   - **Require a pull request before merging**. Required approvals можно
     оставить 0: само требование PR уже не даёт пушить в `main` напрямую.
     Поставишь 1, и тогда смержить можно только после твоего одобрения.
7. **Create**.

Rulesets на бесплатном плане работают для публичных репозиториев, этот
публичный.

## 4. Пригласить Таню

Репозиторий личный, не организация, поэтому у соавтора одна роль: запись
(write). Она может пушить ветки, создавать PR и Issues, но не может менять
настройки, удалять репозиторий или управлять доступом.

**Через сайт:** <https://github.com/dmitry-rukhlenko/tatsiana-fitness-coach-landing/settings/access>
→ **Add people** → логин Тани → **Add to repository**.

**Через терминал** (подставь логин):

```bash
gh api -X PUT repos/dmitry-rukhlenko/tatsiana-fitness-coach-landing/collaborators/ЛОГИН_ТАНИ
```

Пока она не приняла приглашение, в списке она «Pending invite». Проверить:

```bash
gh api repos/dmitry-rukhlenko/tatsiana-fitness-coach-landing/collaborators --jq '.[].login'
```

## 5. Что делает `setup-tanya.sh`

Только macOS. Каждый шаг пропускается, если уже сделан, поэтому повторный
запуск безопасен. Весь вывод дублируется в `~/Desktop/setup-log.txt`.

| Шаг | Что происходит | Что может попросить |
| --- | --- | --- |
| 1 | Git через Apple Command Line Tools | Нажать «Установить» в окне macOS |
| 2 | GitHub CLI: Homebrew, если есть, иначе официальный `.pkg` с <https://github.com/cli/cli/releases> | Пароль Mac для `sudo installer` |
| 3 | `gh auth login --web`, затем `gh auth setup-git` | Ввести код на github.com/login/device |
| 4 | `user.name` (по умолчанию «Tatsiana Rukhlenko») и `user.email` = noreply-адрес GitHub | Enter или другое имя |
| 5 | `gh repo clone` в `~/Coding/tatsiana-fitness-coach-landing`, при повторе `git fetch` | — |
| 6 | Проверка `permissions.push` через API; если нет — открывает страницу приглашений и показывает её логин | — |
| 7 | По желанию Node.js (Homebrew или `.pkg` с nodejs.org, текущая LTS), `npm install`, `npx playwright install chromium` | `y`/`n`, пароль Mac |
| 8 | Открывает Claude.app или страницу загрузки, в конце показывает папку проекта в Finder | — |

Переменные для отладки: `SETUP_DIR` (другая папка), `SETUP_LOG` (другой файл
лога), `SETUP_NO_OPEN=1` (ничего не открывать), `SETUP_NODE=yes|no` (без
вопроса). Прогнан на macOS 20 ноября 2026 с `SETUP_DIR` в отдельную папку:
все 8 шагов прошли.

## 6. Если у Тани Windows

Скрипт не подойдёт. Короткий ручной путь в PowerShell:

```powershell
winget install --id Git.Git -e; winget install --id GitHub.cli -e
```

Затем перезапустить PowerShell и выполнить `gh auth login`, `gh auth setup-git`,
`gh repo clone dmitry-rukhlenko/tatsiana-fitness-coach-landing`. Полный аналог
скрипта под Windows — отдельная задача, если понадобится.

## 7. Приём её работы

Уведомления о PR придут на почту GitHub. Посмотреть и смержить:

```bash
gh pr list --repo dmitry-rukhlenko/tatsiana-fitness-coach-landing
```

```bash
gh pr merge НОМЕР --repo dmitry-rukhlenko/tatsiana-fitness-coach-landing --squash --delete-branch
```

После merge GitHub Pages пересоберёт сайт за минуту-две.

Исходные фото в `original images/` в `.gitignore`; если они ей нужны,
передай отдельно, не через Git.
