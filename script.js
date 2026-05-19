/*
    Tatsiana Rukhlenko landing page behavior.

    The page stays intentionally simple:
    - no external JavaScript dependencies,
    - no analytics,
    - no backend form submission,
    - language switching happens in the browser.
*/

document.addEventListener('DOMContentLoaded', () => {
    const supportedLanguages = ['de', 'en'];
    const defaultLanguage = 'de';
    const contactEmail = 'tatsiana.rukhlenko@gmail.com';

    /*
        Centralized translation data keeps the HTML clean.
        Each key matches a data-i18n attribute in index.html.
    */
    const translations = {
        de: {
            skipLink: 'Zum Inhalt springen',
            menuOpenLabel: 'Menü öffnen',
            menuCloseLabel: 'Menü schließen',
            navForYou: 'Für wen',
            navOffer: 'Beratung',
            navServices: 'Leistungen',
            navAbout: 'Über Tatsiana',
            navFaq: 'FAQ',
            navContact: 'Kontakt',
            navCta: 'Kostenlose Beratung',
            heroEyebrow: 'Mobility & Fitness Coaching',
            heroTitle: 'Freier bewegen. Stärker trainieren. Besser fühlen.',
            heroLead: 'Kostenlose Online-Beratung für Erwachsene, die mehr Bewegungsfreiheit, bessere Haltung und ein Training suchen, das wirklich in den Alltag passt.',
            heroPrimary: 'Beratung anfragen',
            heroSecondary: 'So läuft es ab',
            heroNote: 'Calendly folgt später. Bis dahin kannst du deine Anfrage direkt per Formular senden.',
            trustOneTitle: 'DE / EN',
            trustOneText: 'Beratung auf Deutsch und Englisch',
            trustTwoTitle: 'Mobility first',
            trustTwoText: 'Beweglichkeit, Haltung und Kontrolle',
            trustThreeTitle: 'Individuell',
            trustThreeText: 'Dein Startpunkt, Alltag und Ziel zählen',
            trustFourTitle: 'Qualifikationen',
            trustFourText: 'Details folgen vor dem Launch',
            forYouEyebrow: 'Für wen',
            forYouTitle: 'Für Erwachsene, die sich nicht mehr steif durch den Tag bewegen wollen.',
            forYouLead: 'Der erste Schritt ist keine harte Challenge. Es ist ein klares Gespräch darüber, was dich im Alltag einschränkt und welche Trainingsrichtung sinnvoll ist.',
            benefitOneTitle: 'Mehr Bewegungsfreiheit',
            benefitOneText: 'Für Menschen, die sich im Rücken, in Hüfte, Schultern oder Nacken oft eingeschränkt fühlen.',
            benefitTwoTitle: 'Bessere Haltung',
            benefitTwoText: 'Für alle, die viel sitzen und wieder stabiler, aufrechter und bewusster trainieren möchten.',
            benefitThreeTitle: 'Sicherer Wiedereinstieg',
            benefitThreeText: 'Für Erwachsene, die nach einer Pause wieder anfangen wollen und einen ruhigen, nachvollziehbaren Plan brauchen.',
            servicesEyebrow: 'Leistungen',
            servicesTitle: 'Meine Leistungen',
            servicesLead: 'In der kostenlosen Beratung klären wir, welche Richtung für deinen Körper und deinen Alltag sinnvoll ist.',
            mobilityServicesTitle: 'Mobility-Fokus',
            serviceMobilityCheckTitle: 'Mobility Check',
            serviceMobilityCheckText: 'Wir schauen auf Bewegungsfreiheit, Einschränkungen und die nächsten sinnvollen Schritte.',
            servicePostureTitle: 'Haltung & Beweglichkeit',
            servicePostureText: 'Ein ruhiger Fokus auf Haltung, Körpergefühl und mehr Kontrolle in alltäglicher Bewegung.',
            serviceRestartTitle: 'Wiedereinstieg',
            serviceRestartText: 'Für Erwachsene, die nach einer Pause strukturiert und ohne Überforderung starten möchten.',
            consultationTopicsTitle: 'Themen der Beratung',
            serviceTrainingTitle: 'Training',
            serviceTrainingText: 'Wir besprechen, welche Trainingsform zu deinem Ziel, Level und Alltag passt.',
            serviceOnlineTitle: 'Online Coaching',
            serviceOnlineText: 'Wir klären, ob flexible Online-Begleitung für dich sinnvoll ist und wie sie aussehen könnte.',
            serviceNutritionTitle: 'Nutrition Habits',
            serviceNutritionText: 'Wir sprechen über einfache Ernährungsgewohnheiten, die Training und Alltag unterstützen können.',
            offerEyebrow: 'Kostenlose Beratung',
            offerTitle: 'Erst verstehen, dann trainieren.',
            offerText: 'In der kostenlosen Online-Beratung sprechen wir über deinen Alltag, deine Bewegungseinschränkungen, dein Trainingslevel und deinen nächsten realistischen Schritt. Danach weißt du klarer, welche Art Training zu dir passt.',
            offerPointOne: 'Keine pauschalen Versprechen',
            offerPointTwo: 'Kein Druck, direkt ein Programm zu kaufen',
            offerPointThree: 'Ein ruhiger Blick auf Ziel, Körpergefühl und Routinen',
            offerCta: 'Kostenlose Anfrage senden',
            processEyebrow: 'Ablauf',
            processTitle: 'Von der Anfrage zum klaren nächsten Schritt.',
            processOneTitle: 'Formular senden',
            processOneText: 'Du beschreibst kurz dein Ziel und wie du am liebsten kontaktiert werden möchtest.',
            processTwoTitle: 'Termin abstimmen',
            processTwoText: 'Calendly wird später ergänzt. Bis dahin stimmen wir den Termin per E-Mail ab.',
            processThreeTitle: 'Online sprechen',
            processThreeText: 'Im Gespräch klären wir, was dich bewegt, was dich einschränkt und welche Richtung Sinn ergibt.',
            processFourTitle: 'Nächsten Schritt kennen',
            processFourText: 'Du bekommst eine klare Empfehlung, ohne medizinische Diagnose oder unrealistische Versprechen.',
            aboutEyebrow: 'Über Tatsiana',
            aboutTitle: 'Training soll sich nach mehr Freiheit anfühlen, nicht nach mehr Druck.',
            aboutTextOne: 'Tatsiana Rukhlenko arbeitet mit Menschen, die ihren Körper wieder bewusster bewegen möchten: stärker, flexibler und mit mehr Vertrauen in alltägliche Bewegung.',
            aboutTextTwo: 'Die Beratung ist der Startpunkt. Sie hilft, Ziele zu sortieren, Einschränkungen vorsichtig einzuordnen und einen Trainingsweg zu finden, der nicht überfordert.',
            certTitle: 'Qualifikationen',
            certText: 'Zertifikate und genaue Ausbildungsdetails folgen vor dem öffentlichen Launch.',
            faqEyebrow: 'FAQ',
            faqTitle: 'Häufige Fragen vor der ersten Beratung.',
            faqOneQuestion: 'Ist das nur für sportliche Menschen?',
            faqOneAnswer: 'Nein. Die Beratung ist besonders sinnvoll, wenn du einen verständlichen Einstieg suchst und wissen möchtest, wie du ohne Überforderung anfangen kannst.',
            faqTwoQuestion: 'Geht es um Schmerzbehandlung?',
            faqTwoAnswer: 'Nein. Das Coaching ersetzt keine medizinische Diagnose oder Therapie. Wir sprechen vorsichtig über Bewegungseinschränkungen und alltagstaugliche Trainingsmöglichkeiten.',
            faqThreeQuestion: 'Brauche ich Equipment?',
            faqThreeAnswer: 'Für die erste Beratung nicht. Wenn später ein Training entsteht, wird es an dein Umfeld angepasst: Zuhause, Studio oder einfache Hilfsmittel.',
            faqFourQuestion: 'Wie buche ich aktuell einen Termin?',
            faqFourAnswer: 'Calendly wird später ergänzt. Im MVP sendet das Formular eine vorbereitete E-Mail, danach wird der Termin direkt abgestimmt.',
            contactEyebrow: 'Kontakt',
            contactTitle: 'Direkt erreichbar für deine erste Frage.',
            contactEmailLabel: 'Email:',
            contactInstagramLabel: 'Instagram:',
            consultEyebrow: 'Kostenlose Online-Beratung',
            consultTitle: 'Erzähl kurz, was dich im Moment einschränkt.',
            consultLead: 'Das Formular öffnet dein E-Mail-Programm mit einer vorbereiteten Nachricht an Tatsiana. So bleibt die erste Version ohne Backend und ohne Tracking.',
            calendlyTitle: 'Calendly folgt',
            calendlyText: 'Ein direkter Buchungskalender wird ergänzt, sobald der echte Link bereit ist.',
            formNameLabel: 'Name',
            formNamePlaceholder: 'Dein Name',
            formEmailLabel: 'E-Mail',
            formEmailPlaceholder: 'dein.name@example.com',
            formGoalLabel: 'Was möchtest du verbessern?',
            formGoalPlaceholder: 'Bitte wählen',
            formGoalOne: 'Mobility / Bewegungsfreiheit',
            formGoalTwo: 'Flexibility / Beweglichkeit',
            formGoalThree: 'Posture / Haltung',
            formGoalFour: 'Return to training / Wiedereinstieg',
            formMessageLabel: 'Kurze Nachricht',
            formMessagePlaceholder: 'Was fühlt sich gerade eingeschränkt an? Was möchtest du erreichen?',
            formPrivacyText: 'Ich habe die Datenschutzerklärung gelesen und bin damit einverstanden, dass meine Angaben zur Kontaktaufnahme verwendet werden.',
            formSubmit: 'E-Mail vorbereiten',
            formHelper: 'Deine Daten werden nicht auf dieser Website gespeichert.',
            formHelperReady: 'Dein E-Mail-Programm wird geöffnet. Bitte sende die vorbereitete Nachricht dort ab.',
            formValidationError: 'Bitte fülle alle Pflichtfelder aus und bestätige die Datenschutzerklärung.',
            mailSubject: 'Kostenlose Online-Beratung',
            mailIntro: 'Hallo Tatsiana, ich interessiere mich für eine kostenlose Online-Beratung.',
            mailName: 'Name',
            mailEmail: 'E-Mail',
            mailGoal: 'Ziel',
            mailMessage: 'Nachricht',
            mailPrivacy: 'Datenschutz bestätigt',
            impressumTitle: 'Impressum',
            impressumProvider: 'Angaben gemäß § 5 DDG',
            addressPlaceholder: 'Adresse folgt',
            legalContact: 'Kontakt',
            vatPlaceholder: 'folgt',
            impressumNote: 'Hinweis: Adresse, USt-IdNr. und weitere Pflichtangaben müssen vor dem öffentlichen Launch final geprüft und ergänzt werden.',
            privacyTitle: 'Datenschutzerklärung',
            privacyIntro: 'Diese MVP-Version verwendet keine Analytics-Skripte, keine Marketing-Pixel und keine eingebetteten Drittanbieter-Widgets.',
            privacyForm: 'Wenn du das Formular nutzt, öffnet dein E-Mail-Programm eine vorbereitete Nachricht. Die Verarbeitung erfolgt dann über deine E-Mail-App und den E-Mail-Dienst der Empfängerin.',
            privacyRights: 'Du kannst Auskunft, Berichtigung oder Löschung deiner personenbezogenen Daten verlangen. Die finale Datenschutzerklärung muss vor dem Launch rechtlich geprüft werden.',
            footerTagline: 'Mobility & Fitness Coaching für mehr Bewegungsfreiheit im Alltag.',
            footerImpressum: 'Impressum',
            footerPrivacy: 'Datenschutz'
        },
        en: {
            skipLink: 'Skip to content',
            menuOpenLabel: 'Open menu',
            menuCloseLabel: 'Close menu',
            navForYou: 'Who it helps',
            navOffer: 'Consultation',
            navServices: 'Services',
            navAbout: 'About Tatsiana',
            navFaq: 'FAQ',
            navContact: 'Contact',
            navCta: 'Free consultation',
            heroEyebrow: 'Mobility & Fitness Coaching',
            heroTitle: 'Move freer. Train stronger. Feel better.',
            heroLead: 'A free online consultation for adults who want better movement, better posture, and training that fits real life.',
            heroPrimary: 'Request consultation',
            heroSecondary: 'How it works',
            heroNote: 'Calendly will be added later. For now, you can send your request through the form.',
            trustOneTitle: 'DE / EN',
            trustOneText: 'Consultation in German and English',
            trustTwoTitle: 'Mobility first',
            trustTwoText: 'Flexibility, posture, and control',
            trustThreeTitle: 'Individual',
            trustThreeText: 'Your starting point, routine, and goals matter',
            trustFourTitle: 'Qualifications',
            trustFourText: 'Details will be added before launch',
            forYouEyebrow: 'Who it helps',
            forYouTitle: 'For adults who do not want to move through the day feeling stiff.',
            forYouLead: 'The first step is not a hard challenge. It is a clear conversation about what limits your movement and what kind of training direction makes sense.',
            benefitOneTitle: 'More freedom of movement',
            benefitOneText: 'For people who often feel restricted in the back, hips, shoulders, or neck.',
            benefitTwoTitle: 'Better posture',
            benefitTwoText: 'For anyone who sits a lot and wants to train with more stability, awareness, and control.',
            benefitThreeTitle: 'A safer restart',
            benefitThreeText: 'For adults returning after a break who need a calm, understandable next step.',
            servicesEyebrow: 'Services',
            servicesTitle: 'Services',
            servicesLead: 'In the free consultation, we clarify which direction makes sense for your body and everyday routine.',
            mobilityServicesTitle: 'Mobility focus',
            serviceMobilityCheckTitle: 'Mobility Check',
            serviceMobilityCheckText: 'We look at freedom of movement, limitations, and the next useful steps.',
            servicePostureTitle: 'Posture & Flexibility',
            servicePostureText: 'A calm focus on posture, body awareness, and more control in everyday movement.',
            serviceRestartTitle: 'Return to Training',
            serviceRestartText: 'For adults who want to restart after a break with structure and without overwhelm.',
            consultationTopicsTitle: 'Consultation topics',
            serviceTrainingTitle: 'Training',
            serviceTrainingText: 'We discuss which training direction fits your goal, level, and routine.',
            serviceOnlineTitle: 'Online Coaching',
            serviceOnlineText: 'We clarify whether flexible online support makes sense for you and what it could look like.',
            serviceNutritionTitle: 'Nutrition Habits',
            serviceNutritionText: 'We talk about simple nutrition habits that can support training and everyday life.',
            offerEyebrow: 'Free consultation',
            offerTitle: 'Understand first. Train second.',
            offerText: 'In the free online consultation, we talk about your routine, movement limitations, training level, and next realistic step. After that, you will have a clearer idea of what kind of training fits you.',
            offerPointOne: 'No generic promises',
            offerPointTwo: 'No pressure to buy a program immediately',
            offerPointThree: 'A calm look at goals, body awareness, and routines',
            offerCta: 'Send free request',
            processEyebrow: 'Process',
            processTitle: 'From request to a clear next step.',
            processOneTitle: 'Send the form',
            processOneText: 'You briefly describe your goal and how you prefer to be contacted.',
            processTwoTitle: 'Choose a time',
            processTwoText: 'Calendly will be added later. Until then, the appointment is arranged by email.',
            processThreeTitle: 'Talk online',
            processThreeText: 'In the call, we clarify what moves you, what limits you, and which direction makes sense.',
            processFourTitle: 'Know the next step',
            processFourText: 'You receive a clear recommendation without medical diagnosis or unrealistic promises.',
            aboutEyebrow: 'About Tatsiana',
            aboutTitle: 'Training should feel like more freedom, not more pressure.',
            aboutTextOne: 'Tatsiana Rukhlenko works with people who want to move their bodies with more awareness: stronger, more flexible, and with more confidence in everyday movement.',
            aboutTextTwo: 'The consultation is the starting point. It helps sort goals, carefully discuss limitations, and find a training path that does not overwhelm you.',
            certTitle: 'Qualifications',
            certText: 'Certificates and exact education details will be added before the public launch.',
            faqEyebrow: 'FAQ',
            faqTitle: 'Common questions before the first consultation.',
            faqOneQuestion: 'Is this only for athletic people?',
            faqOneAnswer: 'No. The consultation is especially useful if you want an understandable start and want to begin without overwhelm.',
            faqTwoQuestion: 'Is this pain treatment?',
            faqTwoAnswer: 'No. Coaching does not replace medical diagnosis or therapy. We carefully discuss movement limitations and practical training options.',
            faqThreeQuestion: 'Do I need equipment?',
            faqThreeAnswer: 'Not for the first consultation. If training is developed later, it can be adapted to your setting: home, gym, or simple tools.',
            faqFourQuestion: 'How do I book a time right now?',
            faqFourAnswer: 'Calendly will be added later. In this MVP, the form prepares an email, and the appointment is arranged directly after that.',
            contactEyebrow: 'Contact',
            contactTitle: 'Reach out directly with your first question.',
            contactEmailLabel: 'Email:',
            contactInstagramLabel: 'Instagram:',
            consultEyebrow: 'Free online consultation',
            consultTitle: 'Briefly tell me what limits you right now.',
            consultLead: 'The form opens your email app with a prepared message to Tatsiana. This keeps the first version backend-free and tracking-free.',
            calendlyTitle: 'Calendly coming soon',
            calendlyText: 'A direct booking calendar will be added once the real link is ready.',
            formNameLabel: 'Name',
            formNamePlaceholder: 'Your name',
            formEmailLabel: 'Email',
            formEmailPlaceholder: 'your.name@example.com',
            formGoalLabel: 'What would you like to improve?',
            formGoalPlaceholder: 'Please choose',
            formGoalOne: 'Mobility / freedom of movement',
            formGoalTwo: 'Flexibility',
            formGoalThree: 'Posture',
            formGoalFour: 'Return to training',
            formMessageLabel: 'Short message',
            formMessagePlaceholder: 'What feels limited right now? What would you like to achieve?',
            formPrivacyText: 'I have read the privacy policy and agree that my details may be used to contact me.',
            formSubmit: 'Prepare email',
            formHelper: 'Your data is not stored on this website.',
            formHelperReady: 'Your email app is opening. Please send the prepared message there.',
            formValidationError: 'Please complete all required fields and confirm the privacy policy.',
            mailSubject: 'Free online consultation',
            mailIntro: 'Hello Tatsiana, I am interested in a free online consultation.',
            mailName: 'Name',
            mailEmail: 'Email',
            mailGoal: 'Goal',
            mailMessage: 'Message',
            mailPrivacy: 'Privacy confirmed',
            impressumTitle: 'Imprint',
            impressumProvider: 'Information according to Section 5 DDG',
            addressPlaceholder: 'Address to be added',
            legalContact: 'Contact',
            vatPlaceholder: 'to be added',
            impressumNote: 'Note: address, VAT ID, and any further mandatory legal details must be reviewed and completed before public launch.',
            privacyTitle: 'Privacy Policy',
            privacyIntro: 'This MVP version does not use analytics scripts, marketing pixels, or embedded third-party widgets.',
            privacyForm: 'When you use the form, your email app opens a prepared message. Processing then happens through your email app and the recipient email service.',
            privacyRights: 'You may request access, correction, or deletion of your personal data. The final privacy policy must be legally reviewed before launch.',
            footerTagline: 'Mobility & Fitness Coaching for more freedom of movement in everyday life.',
            footerImpressum: 'Imprint',
            footerPrivacy: 'Privacy'
        }
    };

    const menuButton = document.querySelector('.menu-toggle');
    const siteNav = document.querySelector('.site-nav');
    const languageButtons = document.querySelectorAll('[data-lang-switch]');
    const consultationForm = document.querySelector('#consultation-form');
    const formHelper = document.querySelector('#form-helper');

    function getInitialLanguage() {
        const savedLanguage = localStorage.getItem('preferredLanguage');

        if (supportedLanguages.includes(savedLanguage)) {
            return savedLanguage;
        }

        return defaultLanguage;
    }

    function translatePage(language) {
        const dictionary = translations[language] || translations[defaultLanguage];

        document.documentElement.lang = language;

        document.querySelectorAll('[data-i18n]').forEach((element) => {
            const key = element.dataset.i18n;
            if (dictionary[key]) {
                element.textContent = dictionary[key];
            }
        });

        document.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {
            const key = element.dataset.i18nPlaceholder;
            if (dictionary[key]) {
                element.placeholder = dictionary[key];
            }
        });

        document.querySelectorAll('[data-i18n-aria-label]').forEach((element) => {
            const key = element.dataset.i18nAriaLabel;
            if (dictionary[key]) {
                element.setAttribute('aria-label', dictionary[key]);
            }
        });

        languageButtons.forEach((button) => {
            const isActive = button.dataset.langSwitch === language;
            button.classList.toggle('is-active', isActive);
            button.setAttribute('aria-pressed', String(isActive));
        });

        localStorage.setItem('preferredLanguage', language);
    }

    function closeMobileMenu() {
        document.body.classList.remove('menu-open');
        siteNav.classList.remove('is-open');
        menuButton.classList.remove('is-open');
        menuButton.setAttribute('aria-expanded', 'false');
        menuButton.setAttribute('aria-label', translations[getInitialLanguage()].menuOpenLabel);
    }

    function toggleMobileMenu() {
        const isOpen = siteNav.classList.toggle('is-open');
        document.body.classList.toggle('menu-open', isOpen);
        menuButton.classList.toggle('is-open', isOpen);
        menuButton.setAttribute('aria-expanded', String(isOpen));

        const language = getInitialLanguage();
        const labelKey = isOpen ? 'menuCloseLabel' : 'menuOpenLabel';
        menuButton.setAttribute('aria-label', translations[language][labelKey]);
    }

    function buildMailtoUrl(formData, language) {
        const dictionary = translations[language] || translations[defaultLanguage];
        const subject = encodeURIComponent(dictionary.mailSubject);
        const bodyLines = [
            dictionary.mailIntro,
            '',
            `${dictionary.mailName}: ${formData.get('name')}`,
            `${dictionary.mailEmail}: ${formData.get('email')}`,
            `${dictionary.mailGoal}: ${formData.get('goal')}`,
            '',
            `${dictionary.mailMessage}:`,
            formData.get('message'),
            '',
            `${dictionary.mailPrivacy}: yes`
        ];

        return `mailto:${contactEmail}?subject=${subject}&body=${encodeURIComponent(bodyLines.join('\n'))}`;
    }

    function handleFormSubmit(event) {
        event.preventDefault();

        if (!consultationForm.checkValidity()) {
            const language = getInitialLanguage();
            formHelper.textContent = translations[language].formValidationError;
            consultationForm.reportValidity();
            return;
        }

        const language = getInitialLanguage();
        const formData = new FormData(consultationForm);
        formHelper.textContent = translations[language].formHelperReady;

        window.location.href = buildMailtoUrl(formData, language);
    }

    function initializeRevealAnimation() {
        const revealElements = document.querySelectorAll('.reveal');

        if (!('IntersectionObserver' in window)) {
            revealElements.forEach((element) => element.classList.add('is-visible'));
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.14 });

        revealElements.forEach((element) => observer.observe(element));
    }

    menuButton.addEventListener('click', toggleMobileMenu);

    siteNav.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', closeMobileMenu);
    });

    languageButtons.forEach((button) => {
        button.addEventListener('click', () => {
            translatePage(button.dataset.langSwitch);
            closeMobileMenu();
        });
    });

    consultationForm.addEventListener('submit', handleFormSubmit);

    translatePage(getInitialLanguage());
    initializeRevealAnimation();
});
