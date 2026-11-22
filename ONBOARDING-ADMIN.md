# Подключение соавтора: шпаргалка для владельца репозитория

Пара к `ONBOARDING.md` (инструкция для Тани) и `CLAUDE-SETUP.md`
(инструкция, которую Таня отдаёт Claude). Здесь то, что делаешь ты.

У Тани Windows, поэтому её путь — без командной строки: три обычных
установщика (Claude, Git, GitHub Desktop), вход в GitHub через браузер и
кнопка Clone. Для Mac в конце `ONBOARDING.md` остался короткий раздел со
скриптом `setup-tanya.sh`.

## 1. Порядок действий

1. **`main` защищена** (пункт 3) — уже сделано 20 ноября 2026.
2. **Отправить Тане архив и сообщение** (пункт 2) и дождаться её логина
   GitHub.
3. **Пригласить её** в репозиторий (пункт 4).
4. Дальше она идёт по инструкции сама или вместе с Claude. Если что-то не
   получается, она пришлёт скриншот.

Архив `handoff-tanya/Таня — старт работы над сайтом.zip` лежит локально и в
Git не попадает. Внутри два файла:

| Файл | Для чего |
| --- | --- |
| `Инструкция для Тани.pdf` | `ONBOARDING.md` в виде PDF: открывается двойным щелчком, ссылки кликабельные |
| `CLAUDE-SETUP.md` | Инструкция для Claude. Таня перетаскивает её в чат Claude Code, и Claude ведёт её по шагам и проверяет результат |

Шаги 1–3 (аккаунт GitHub, Claude, Git) Таня делает сама: вкладка Code на
Windows без Git не запускается. Дальше можно с Claude.

PDF пересобирается из `ONBOARDING.md` через Playwright, который уже есть в
проекте; если инструкция изменится, попроси Claude пересобрать архив.
Архив собирать через Python `zipfile`, а не через «Сжать» в Finder или
`ditto`: они не ставят флаг UTF-8 для имён, и Проводник Windows покажет
русские имена файлов нечитаемыми символами.

## 2. Текст сообщения для Тани

Можно отправить как есть, приложив архив.

```text
Таня, привет! Чтобы ты могла править сайт вместе с Claude, нужно один раз
подготовить компьютер. Это примерно 30–40 минут, командную строку открывать
не нужно — только скачать три программы и нажать кнопки.

В архиве два файла:
• «Инструкция для Тани.pdf» — всё по шагам, с объяснением каждого слова;
• «CLAUDE-SETUP.md» — инструкция для Claude. Когда поставишь Claude и Git
  (шаги 2 и 3 в PDF), открой в Claude вкладку Code, перетащи туда этот файл
  и напиши «Проведи меня по этой инструкции» — дальше Claude поможет сам.

Самое первое: заведи аккаунт на https://github.com/signup и пришли мне свой
логин. Я добавлю тебя в проект, придёт письмо «invited you to collaborate» —
нажми там Accept.

Если что-то не получается — пришли скриншот.
```

## 3. Защитить `main`

GitHub Pages публикует сайт из ветки `main`, папка `/`. Без защиты любой
соавтор может запушить в неё напрямую, и правка через минуту окажется на
живом сайте. Инструкция велит Тане работать через ветки и pull request, но
надёжнее, чтобы это обеспечивал GitHub.

**Сделано 20 ноября 2026:** ruleset `protect-main` создан через API и активен
(<https://github.com/dmitry-rukhlenko/tatsiana-fitness-coach-landing/rules/27721864>).
Шаги ниже оставлены на случай, если его придётся пересоздать.

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

## 5. Путь для Windows: что где лежит

| Что | Где | Зачем |
| --- | --- | --- |
| Git for Windows | <https://git-scm.com/downloads/win>, все настройки по умолчанию | Нужен Claude Code на Windows; в комплекте Git Credential Manager, он даёт вход для `git push` через браузер |
| GitHub Desktop | <https://desktop.github.com/download/> | Вход в GitHub, имя и почта для коммитов (экран Configure Git), клон по кнопке |
| Папка проекта | `C:\Users\<имя>\Documents\GitHub\tatsiana-fitness-coach-landing` — путь GitHub Desktop по умолчанию, может оказаться в OneDrive | Её Таня открывает в Claude Code |

`gh` у неё нет. Её Claude пушит ветку через Git Credential Manager и даёт
ссылку `.../compare/main...<ветка>?expand=1`, а Таня нажимает **Create pull
request** на сайте. Это записано в конце `CLAUDE-SETUP.md`.

Почта в коммитах берётся из экрана Configure Git в GitHub Desktop.
Инструкция просит выбрать адрес на `users.noreply.github.com`, если он есть
в списке. Если его нет, в коммитах будет её настоящая почта: репозиторий
публичный, так что это видно всем. Включить скрытие можно в её настройках
GitHub: Settings → Emails → Keep my email addresses private.

Путь Windows вживую не прогонялся: на этом Mac нет Windows. Кнопки и
названия экранов описаны по документации установщиков; если у Тани что-то
выглядит иначе, поправь инструкцию по её скриншоту.

## 6. Скрипт `setup-tanya.sh` (только Mac)

Нужен, только если Таня когда-нибудь будет работать с Mac. Каждый шаг
пропускается, если уже сделан, поэтому повторный запуск безопасен. Весь
вывод дублируется в `~/Desktop/setup-log.txt`.

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
