# Tatsiana Rukhlenko Landing - Future Plan

Этот план фиксирует задачи, которые нужно выполнить после ревью статического MVP.

## 1. Перед публичным запуском

1.1. Заменить `Adresse folgt` на реальный рабочий адрес, который нужен для немецкого Impressum.

1.2. Заменить `USt-IdNr.: folgt` только после подтверждения настоящего VAT ID. Не использовать временное значение `123456789`.

1.3. Добавить проверенные данные о квалификациях, сертификатах и обучении Tatsiana.

1.4. Финально проверить `Impressum` и `Datenschutzerklärung` у квалифицированного немецкого legal/privacy специалиста.

1.5. Добавить реальную Calendly-ссылку, когда она будет готова. До этого не показывать Calendly в публичном тексте сайта.

## 2. Запись на консультацию и формы

2.1. Решить, как будет работать Calendly: открываться внешней ссылкой или встраиваться прямо на страницу.

2.2. Если Calendly будет встроен на страницу, обновить `Datenschutzerklärung`, потому что будет загружаться сторонний виджет.

2.3. Рассмотреть замену текущего `mailto:` fallback на полноценный form service или backend endpoint.

2.4. Если будет использоваться form service, документировать, где хранятся данные формы и как долго они сохраняются.

## 3. Аналитика и согласие пользователя

3.1. В MVP сейчас намеренно нет аналитики и трекинга.

3.2. Возможные варианты аналитики на будущее:

3.2.1. Cloudflare Web Analytics как бесплатный privacy-friendly вариант.

3.2.2. Plausible, Fathom или Vercel Analytics как privacy-friendly варианты для понимания трафика.

3.2.3. Google Analytics или Meta Pixel только если понадобятся реклама, remarketing или более сложный marketing tracking.

3.3. Если выбран Cloudflare Web Analytics и сайт не размещён через Cloudflare Pages, использовать вариант 1: вручную добавить Cloudflare JavaScript snippet перед `</body>` в `index.html` и `impressum.html` после получения реального `data-cf-beacon` token.

3.4. Если добавляется Cloudflare Web Analytics, включить этот раздел в `Datenschutzerklärung` и юридически проверить его перед запуском:

`Wir verwenden Cloudflare Web Analytics zur anonymisierten Auswertung der Seitennutzung. Cloudflare Web Analytics verwendet keine Cookies und erhebt nach Angaben von Cloudflare keine personenbezogenen Daten der Besucher.`

3.5. Если добавляются analytics, pixels, maps, videos или embedded widgets, реализовать consent до загрузки этих инструментов.

3.6. Добавить cookie/settings control, чтобы пользователь мог позже изменить своё согласие.

## 4. Развитие контента

4.1. Добавлять отзывы клиентов только с явным разрешением.

4.2. Добавлять before/after или transformation content только с явным письменным согласием.

4.3. Добавить детали услуг, пакетов или программ после того, как Tatsiana подтвердит точное предложение.

4.4. Позже добавить блог или короткие статьи для SEO по темам mobility, posture, flexibility и beginner-friendly training.

## 5. Публикация и инфраструктура

5.1. Выбрать hosting: static hosting, Vercel, Netlify или другой провайдер.

5.2. Подключить domain, SSL и production metadata.

5.3. Перед запуском проверить mobile, desktop, accessibility, language switching и legal footer links.
