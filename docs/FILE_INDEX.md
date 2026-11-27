# What each file does

Use the [project guide](DEVELOPER_MAP.md) to learn how the website works. Use this list to find one file and see what to change there.

Each folder name is a heading. File links open the code. The last column shows files it loads or functions you can look for. All paths start from the main project folder.

Images are explained at the end. `.env` is private and is not listed. Git’s own files and Python cache files are also left out.

## Main project folder

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [.dockerignore](../.dockerignore) | Lists files left out when Docker copies the project. | — |
| [.editorconfig](../.editorconfig) | Sets shared spacing and text-file settings for editors. | — |
| [.env.example](../.env.example) | Shows the setting names to copy into your own .env file. | — |
| [.gitignore](../.gitignore) | Lists files Git should not save, such as passwords and cache files. | — |
| [Dockerfile](../Dockerfile) | Tells Docker how to install and start the website. | — |
| [README.md](../README.md) | Explains how to start the website and run checks. | — |
| [SEO_MAINTENANCE.md](../SEO_MAINTENANCE.md) | Explains how to keep page search information up to date. | — |
| [app.py](../app.py) | Starts the website and makes it available to the web server. | — |
## backend

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [__init__.py](../backend/__init__.py) | Loads settings, sets up Flask and connects page links. | `create_app()` |
| [config.py](../backend/config.py) | Reads settings and supplies their default values. | — |
## backend/data

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [__init__.py](../backend/data/__init__.py) | Marks this folder as the place for page data. | — |
| [australia.py](../backend/data/australia.py) | Holds the Australian university cards, numbers and steps. | `get_australia_content()` |
| [destinations.py](../backend/data/destinations.py) | Holds university and country lists for destination pages. | `get_usa_universities()`<br>`get_uk_universities()`<br>`get_canada_universities()`<br>`get_europe_countries()`<br>`get_more_countries()` |
| [sitemap.py](../backend/data/sitemap.py) | Lists page links and their priorities for the sitemap. | `get_sitemap_pages()` |
## backend/routes

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [__init__.py](../backend/routes/__init__.py) | Connects all groups of page handlers. | `register_routes()` |
| [booking.py](../backend/routes/booking.py) | Checks the booking form, sends it to the email code and shows a message. | `_render_booking()`<br>`booking_page()`<br>`register_routes()` |
| [destinations.py](../backend/routes/destinations.py) | Opens destination pages and gives them their lists. | `usa_destination()`<br>`uk_destination()`<br>`canada_destination()`<br>`europe_destination()`<br>`more_destinations()`<br>`australia_destination()`<br>`register_routes()` |
| [pages.py](../backend/routes/pages.py) | Opens the homepage and IELTS/PTE pages. | `landing_page()`<br>`ielts_preparation()`<br>`pte_preparation()`<br>`register_routes()` |
| [redirects.py](../backend/routes/redirects.py) | Sends old page links to the right current pages. | `ielts_preparation_legacy()`<br>`pte_preparation_legacy()`<br>`legacy_university_of_melbourne()`<br>`legacy_australian_national_university()`<br>`legacy_university_of_sydney()`<br>`legacy_unsw_sydney()`<br>`legacy_monash_university()`<br>`legacy_university_of_queensland()`<br>`register_routes()` |
| [seo.py](../backend/routes/seo.py) | Returns the sitemap and search-engine rules. | `robots_txt()`<br>`sitemap_xml()`<br>`register_routes()` |
| [universities.py](../backend/routes/universities.py) | Opens the six university pages. | `university_of_melbourne()`<br>`australian_national_university()`<br>`university_of_sydney()`<br>`unsw_sydney()`<br>`monash_university()`<br>`university_of_queensland()`<br>`register_routes()` |
## backend/services

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [__init__.py](../backend/services/__init__.py) | Marks this folder as the place for email and spam-check code. | — |
| [booking_email.py](../backend/services/booking_email.py) | Builds and sends booking and confirmation emails. | `_valid_reply_to()`<br>`send_booking_email()` |
| [turnstile.py](../backend/services/turnstile.py) | Checks the visitor’s Turnstile response to help stop spam. | `turnstile_is_configured()`<br>`validate_turnstile()` |
## docs

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [DEVELOPER_MAP.md](../docs/DEVELOPER_MAP.md) | Explains how the whole project works and where to make changes. | — |
| [FILE_INDEX.md](../docs/FILE_INDEX.md) | Lists files and explains what each one does. | — |
## Main project folder

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [requirements-dev.txt](../requirements-dev.txt) | Lists extra packages used for checks and formatting. | — |
| [requirements.txt](../requirements.txt) | Lists Python packages needed to run the website. | — |
## static/css/animations

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [accessibility-and-dark-mode.css](../static/css/animations/accessibility-and-dark-mode.css) | Sets styles for hidden heading and page-link spacing and dark mode. | — |
| [ambient-effects.css](../static/css/animations/ambient-effects.css) | Sets styles for gentle background movement effects. | — |
| [animation-classes.css](../static/css/animations/animation-classes.css) | Sets styles for animation classes. | — |
| [attention-keyframes.css](../static/css/animations/attention-keyframes.css) | Sets styles for attention effects movement steps. | — |
| [bounce-and-slide.css](../static/css/animations/bounce-and-slide.css) | Sets styles for bounce and slide. | — |
| [buttons.css](../static/css/animations/buttons.css) | Sets styles for buttons. | — |
| [cards.css](../static/css/animations/cards.css) | Sets styles for cards. | — |
| [reveal-classes.css](../static/css/animations/reveal-classes.css) | Sets styles for showing items classes. | — |
| [rotate-and-scale.css](../static/css/animations/rotate-and-scale.css) | Sets styles for rotate and scale. | — |
| [scroll-reveals.css](../static/css/animations/scroll-reveals.css) | Sets styles for scroll reveals. | — |
| [sections-and-parallax.css](../static/css/animations/sections-and-parallax.css) | Sets styles for sections and scrolling effects. | — |
| [shapes.css](../static/css/animations/shapes.css) | Sets styles for shapes. | — |
| [swing-flip-elastic.css](../static/css/animations/swing-flip-elastic.css) | Sets styles for swing flip elastic. | — |
| [text-and-icons.css](../static/css/animations/text-and-icons.css) | Sets styles for text and icons. | — |
| [timing.css](../static/css/animations/timing.css) | Sets styles for timing. | — |
| [variables.css](../static/css/animations/variables.css) | Sets styles for shared values. | — |
## static/css

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [base-inline.css](../static/css/base-inline.css) | Loads the smaller style files listed here, in order. | [layout/foundation.css](../static/css/layout/foundation.css)<br>[layout/footer.css](../static/css/layout/footer.css)<br>[layout/reveal-and-motion.css](../static/css/layout/reveal-and-motion.css)<br>[layout/cards-and-process.css](../static/css/layout/cards-and-process.css)<br>[layout/requirements.css](../static/css/layout/requirements.css)<br>[layout/contact-widgets.css](../static/css/layout/contact-widgets.css)<br>[layout/navigation-accordion.css](../static/css/layout/navigation-accordion.css) |
## static/css/booking

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [editorial-layout.css](../static/css/booking/editorial-layout.css) | Sets styles for page design layout. | — |
| [form-and-fields.css](../static/css/booking/form-and-fields.css) | Sets styles for form and fields. | — |
| [foundation.css](../static/css/booking/foundation.css) | Sets styles for basic styles. | — |
## static/css/home

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [budget-guidance.css](../static/css/home/budget-guidance.css) | Sets styles for budget guidance. | — |
| [consultation.css](../static/css/home/consultation.css) | Sets styles for consultation section. | — |
| [destination-typography.css](../static/css/home/destination-typography.css) | Sets styles for destination text sizes and fonts. | — |
| [destinations.css](../static/css/home/destinations.css) | Sets styles for destinations. | — |
| [hero.css](../static/css/home/hero.css) | Sets styles for opening section. | — |
| [mobile-and-expansion.css](../static/css/home/mobile-and-expansion.css) | Sets styles for mobile and expansion. | — |
| [services-foundation.css](../static/css/home/services-foundation.css) | Sets styles for services basic styles. | — |
| [services-presentation.css](../static/css/home/services-presentation.css) | Loads the smaller style files listed here, in order. | [services/flow-and-motion.css](../static/css/home/services/flow-and-motion.css)<br>[services/stage.css](../static/css/home/services/stage.css)<br>[services/card-stack.css](../static/css/home/services/card-stack.css) |
## static/css/home/services

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [card-stack.css](../static/css/home/services/card-stack.css) | Sets styles for card stack. | — |
| [flow-and-motion.css](../static/css/home/services/flow-and-motion.css) | Sets styles for flow and motion. | — |
| [stage.css](../static/css/home/services/stage.css) | Sets styles for stage. | — |
## static/css/home

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [test-preparation.css](../static/css/home/test-preparation.css) | Sets styles for test preparation. | — |
| [university-cards.css](../static/css/home/university-cards.css) | Sets styles for university cards. | — |
## static/css

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [landing-common.css](../static/css/landing-common.css) | Holds styles shared by university pages. | — |
| [layout-overrides.css](../static/css/layout-overrides.css) | Adjusts shared styles after earlier style files load. | — |
## static/css/layout

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [cards-and-process.css](../static/css/layout/cards-and-process.css) | Sets styles for cards and process. | — |
| [contact-widgets.css](../static/css/layout/contact-widgets.css) | Sets styles for contact widgets. | — |
| [footer.css](../static/css/layout/footer.css) | Sets styles for footer. | — |
| [foundation.css](../static/css/layout/foundation.css) | Sets styles for basic styles. | — |
| [navigation-accordion.css](../static/css/layout/navigation-accordion.css) | Sets styles for navigation open-and-close menu. | — |
| [requirements.css](../static/css/layout/requirements.css) | Sets styles for requirements. | — |
| [reveal-and-motion.css](../static/css/layout/reveal-and-motion.css) | Sets styles for showing items and motion. | — |
## static/css/pages

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [booking.css](../static/css/pages/booking.css) | Loads the smaller style files listed here, in order. | [../booking/foundation.css](../static/css/pages/../booking/foundation.css)<br>[../booking/editorial-layout.css](../static/css/pages/../booking/editorial-layout.css)<br>[../booking/form-and-fields.css](../static/css/pages/../booking/form-and-fields.css) |
| [home.css](../static/css/pages/home.css) | Loads the smaller style files listed here, in order. | [../home/hero.css](../static/css/pages/../home/hero.css)<br>[../home/university-cards.css](../static/css/pages/../home/university-cards.css)<br>[../home/services-foundation.css](../static/css/pages/../home/services-foundation.css)<br>[../home/mobile-and-expansion.css](../static/css/pages/../home/mobile-and-expansion.css)<br>[../home/destinations.css](../static/css/pages/../home/destinations.css)<br>[../home/budget-guidance.css](../static/css/pages/../home/budget-guidance.css)<br>[../home/destination-typography.css](../static/css/pages/../home/destination-typography.css)<br>[../home/test-preparation.css](../static/css/pages/../home/test-preparation.css)<br>[../home/services-presentation.css](../static/css/pages/../home/services-presentation.css)<br>[../home/consultation.css](../static/css/pages/../home/consultation.css) |
## static/css

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [premium-animations.css](../static/css/premium-animations.css) | Loads the smaller style files listed here, in order. | [animations/variables.css](../static/css/animations/variables.css)<br>[animations/scroll-reveals.css](../static/css/animations/scroll-reveals.css)<br>[animations/ambient-effects.css](../static/css/animations/ambient-effects.css)<br>[animations/bounce-and-slide.css](../static/css/animations/bounce-and-slide.css)<br>[animations/rotate-and-scale.css](../static/css/animations/rotate-and-scale.css)<br>[animations/swing-flip-elastic.css](../static/css/animations/swing-flip-elastic.css)<br>[animations/attention-keyframes.css](../static/css/animations/attention-keyframes.css)<br>[animations/shapes.css](../static/css/animations/shapes.css)<br>[animations/reveal-classes.css](../static/css/animations/reveal-classes.css)<br>[animations/animation-classes.css](../static/css/animations/animation-classes.css)<br>[animations/timing.css](../static/css/animations/timing.css)<br>[animations/cards.css](../static/css/animations/cards.css)<br>[animations/buttons.css](../static/css/animations/buttons.css)<br>[animations/text-and-icons.css](../static/css/animations/text-and-icons.css)<br>[animations/sections-and-parallax.css](../static/css/animations/sections-and-parallax.css)<br>[animations/accessibility-and-dark-mode.css](../static/css/animations/accessibility-and-dark-mode.css) |
| [responsive.css](../static/css/responsive.css) | Loads the smaller style files listed here, in order. | [responsive/viewport.css](../static/css/responsive/viewport.css)<br>[responsive/tablet.css](../static/css/responsive/tablet.css)<br>[responsive/phone.css](../static/css/responsive/phone.css)<br>[responsive/small-phone.css](../static/css/responsive/small-phone.css)<br>[responsive/visibility.css](../static/css/responsive/visibility.css)<br>[responsive/hero-pagination.css](../static/css/responsive/hero-pagination.css)<br>[responsive/navigation.css](../static/css/responsive/navigation.css)<br>[responsive/contact-widgets.css](../static/css/responsive/contact-widgets.css) |
## static/css/responsive

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [contact-widgets.css](../static/css/responsive/contact-widgets.css) | Sets styles for contact widgets. | — |
| [hero-pagination.css](../static/css/responsive/hero-pagination.css) | Sets styles for opening section pagination. | — |
| [navigation.css](../static/css/responsive/navigation.css) | Sets styles for navigation. | — |
| [phone.css](../static/css/responsive/phone.css) | Sets styles for phone. | — |
| [small-phone.css](../static/css/responsive/small-phone.css) | Sets styles for small phone. | — |
| [tablet.css](../static/css/responsive/tablet.css) | Sets styles for tablet. | — |
| [viewport.css](../static/css/responsive/viewport.css) | Sets styles for screen size. | — |
| [visibility.css](../static/css/responsive/visibility.css) | Sets styles for visibility. | — |
## static/css

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [university-editorial.css](../static/css/university-editorial.css) | Sets shared university page spacing and image display. | — |
## static/js

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [booking.js](../static/js/booking.js) | Controls the date picker and the preferred test/destination labels. | — |
## static/js/home

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [budget-guidance.js](../static/js/home/budget-guidance.js) | Moves the destination section after budget guidance. | — |
| [hero-carousel.js](../static/js/home/hero-carousel.js) | Controls homepage slides, arrows, dots and touch actions. | — |
| [mobile-content.js](../static/js/home/mobile-content.js) | Controls show-more buttons and shorter text on phones. | — |
| [services.js](../static/js/home/services.js) | Controls service tabs, cards and automatic changes. | — |
## static/js/layout

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [contact-widgets.js](../static/js/layout/contact-widgets.js) | Opens and closes the booking and WhatsApp menus. | — |
| [expandable-content.js](../static/js/layout/expandable-content.js) | Keeps the older show-more button action. | — |
| [hero-text.js](../static/js/layout/hero-text.js) | Controls the opening text movement effects. | — |
| [page-controls.js](../static/js/layout/page-controls.js) | Adds icons and keeps the older menu-button action. | — |
| [scroll-reveals.js](../static/js/layout/scroll-reveals.js) | Shows page items as they come into view. | — |
| [text-formatting.js](../static/js/layout/text-formatting.js) | Gives the & sign its special text style. | — |
## static/js

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [premium-animations.js](../static/js/premium-animations.js) | Holds shared helpers for movement effects on university pages. | — |
| [premium-pages.js](../static/js/premium-pages.js) | Controls page changes, card hover effects and browser Back behavior. | — |
| [tailwind-config.js](../static/js/tailwind-config.js) | Sets the colors and other theme values used by Tailwind. | — |
| [university-interactions.js](../static/js/university-interactions.js) | Shows university page effects, counters and smooth scrolling. | — |
## templates

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [_destination_guide_styles.html](../templates/_destination_guide_styles.html) | Adds the shared destination styles to the page. | [styles/destinations/guide.css.jinja](../templates/styles/destinations/guide.css.jinja) |
| [anu_landing.html](../templates/anu_landing.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[partials/universities/anu/styles.html](../templates/partials/universities/anu/styles.html)<br>[partials/schema/anu_landing-faq.html](../templates/partials/schema/anu_landing-faq.html)<br>[partials/universities/anu/introduction.html](../templates/partials/universities/anu/introduction.html)<br>[partials/universities/anu/study-and-admissions.html](../templates/partials/universities/anu/study-and-admissions.html)<br>[partials/universities/anu/student-life-and-process.html](../templates/partials/universities/anu/student-life-and-process.html)<br>[partials/universities/anu/faq-and-consultation.html](../templates/partials/universities/anu/faq-and-consultation.html) |
| [australia.html](../templates/australia.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[_destination_guide_styles.html](../templates/_destination_guide_styles.html)<br>[partials/destinations/australia/overview.html](../templates/partials/destinations/australia/overview.html)<br>[partials/destinations/australia/work-and-lifestyle.html](../templates/partials/destinations/australia/work-and-lifestyle.html)<br>[partials/destinations/australia/settling.html](../templates/partials/destinations/australia/settling.html)<br>[partials/destinations/australia/institutions.html](../templates/partials/destinations/australia/institutions.html)<br>[partials/destinations/australia/consultation.html](../templates/partials/destinations/australia/consultation.html) |
| [base.html](../templates/base.html) | Holds the shared page frame, search details, menus, footer and file loading. | [partials/layout/navigation.html](../templates/partials/layout/navigation.html)<br>[partials/layout/footer.html](../templates/partials/layout/footer.html)<br>[partials/layout/mobile-navigation.html](../templates/partials/layout/mobile-navigation.html)<br>[partials/layout/mobile-navigation-script.html](../templates/partials/layout/mobile-navigation-script.html)<br>[partials/layout/contact-widgets.html](../templates/partials/layout/contact-widgets.html) |
| [booking.html](../templates/booking.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[partials/booking/introduction.html](../templates/partials/booking/introduction.html)<br>[partials/booking/form.html](../templates/partials/booking/form.html)<br>[partials/booking/next-steps.html](../templates/partials/booking/next-steps.html) |
| [canada.html](../templates/canada.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[_destination_guide_styles.html](../templates/_destination_guide_styles.html)<br>[styles/destinations/accessibility.css.jinja](../templates/styles/destinations/accessibility.css.jinja)<br>[partials/destinations/canada/overview.html](../templates/partials/destinations/canada/overview.html)<br>[partials/destinations/canada/work-and-lifestyle.html](../templates/partials/destinations/canada/work-and-lifestyle.html)<br>[partials/destinations/canada/settling.html](../templates/partials/destinations/canada/settling.html)<br>[partials/destinations/canada/institutions.html](../templates/partials/destinations/canada/institutions.html)<br>[partials/destinations/canada/consultation.html](../templates/partials/destinations/canada/consultation.html) |
## templates/components

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [preparation.html](../templates/components/preparation.html) | Holds the shared enquiry button and section box used by IELTS/PTE pages. | — |
## templates

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [europe.html](../templates/europe.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[_destination_guide_styles.html](../templates/_destination_guide_styles.html)<br>[styles/destinations/accessibility.css.jinja](../templates/styles/destinations/accessibility.css.jinja)<br>[partials/destinations/europe/overview.html](../templates/partials/destinations/europe/overview.html)<br>[partials/destinations/europe/work-and-lifestyle.html](../templates/partials/destinations/europe/work-and-lifestyle.html)<br>[partials/destinations/europe/settling.html](../templates/partials/destinations/europe/settling.html)<br>[partials/destinations/europe/institutions.html](../templates/partials/destinations/europe/institutions.html)<br>[partials/destinations/europe/consultation.html](../templates/partials/destinations/europe/consultation.html) |
| [ielts_preparation.html](../templates/ielts_preparation.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[components/preparation.html](../templates/components/preparation.html)<br>[components/preparation.html](../templates/components/preparation.html)<br>[partials/preparation/ielts/test-and-skills.html](../templates/partials/preparation/ielts/test-and-skills.html)<br>[partials/preparation/ielts/practice-and-classes.html](../templates/partials/preparation/ielts/practice-and-classes.html)<br>[partials/preparation/ielts/resources-and-questions.html](../templates/partials/preparation/ielts/resources-and-questions.html)<br>[partials/preparation/ielts/enquiry.html](../templates/partials/preparation/ielts/enquiry.html) |
| [index.html](../templates/index.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[partials/home/hero.html](../templates/partials/home/hero.html)<br>[partials/home/university-showcase.html](../templates/partials/home/university-showcase.html)<br>[partials/home/destinations.html](../templates/partials/home/destinations.html)<br>[partials/home/budget-guidance.html](../templates/partials/home/budget-guidance.html)<br>[partials/home/test-preparation.html](../templates/partials/home/test-preparation.html)<br>[partials/home/about.html](../templates/partials/home/about.html)<br>[partials/home/why-choose-us.html](../templates/partials/home/why-choose-us.html)<br>[partials/home/services.html](../templates/partials/home/services.html)<br>[partials/home/consultation.html](../templates/partials/home/consultation.html) |
| [melbourne_landing.html](../templates/melbourne_landing.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[partials/universities/melbourne/styles.html](../templates/partials/universities/melbourne/styles.html)<br>[partials/schema/melbourne_landing-faq.html](../templates/partials/schema/melbourne_landing-faq.html)<br>[partials/universities/melbourne/styles-editorial.html](../templates/partials/universities/melbourne/styles-editorial.html)<br>[partials/universities/melbourne/introduction.html](../templates/partials/universities/melbourne/introduction.html)<br>[partials/universities/melbourne/study-and-admissions.html](../templates/partials/universities/melbourne/study-and-admissions.html)<br>[partials/universities/melbourne/student-life-and-process.html](../templates/partials/universities/melbourne/student-life-and-process.html)<br>[partials/universities/melbourne/faq-and-consultation.html](../templates/partials/universities/melbourne/faq-and-consultation.html) |
| [monash_landing.html](../templates/monash_landing.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[partials/universities/monash/styles.html](../templates/partials/universities/monash/styles.html)<br>[partials/universities/monash/introduction.html](../templates/partials/universities/monash/introduction.html)<br>[partials/universities/monash/study-and-admissions.html](../templates/partials/universities/monash/study-and-admissions.html)<br>[partials/universities/monash/student-life-and-process.html](../templates/partials/universities/monash/student-life-and-process.html)<br>[partials/universities/monash/faq-and-consultation.html](../templates/partials/universities/monash/faq-and-consultation.html) |
| [more.html](../templates/more.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[_destination_guide_styles.html](../templates/_destination_guide_styles.html)<br>[styles/destinations/accessibility.css.jinja](../templates/styles/destinations/accessibility.css.jinja)<br>[partials/destinations/more/overview.html](../templates/partials/destinations/more/overview.html)<br>[partials/destinations/more/work-and-lifestyle.html](../templates/partials/destinations/more/work-and-lifestyle.html)<br>[partials/destinations/more/settling.html](../templates/partials/destinations/more/settling.html)<br>[partials/destinations/more/institutions.html](../templates/partials/destinations/more/institutions.html)<br>[partials/destinations/more/consultation.html](../templates/partials/destinations/more/consultation.html) |
## templates/partials/booking

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [form.html](../templates/partials/booking/form.html) | Booking fields, error messages and spam-check boxes. | — |
| [introduction.html](../templates/partials/booking/introduction.html) | Opening text and an overview. | — |
| [next-steps.html](../templates/partials/booking/next-steps.html) | Steps explaining what happens after booking. | — |
## templates/partials/destinations/australia

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [consultation.html](../templates/partials/destinations/australia/consultation.html) | The closing message and booking link. | — |
| [institutions.html](../templates/partials/destinations/australia/institutions.html) | The university or country list shown on this page. | — |
| [overview.html](../templates/partials/destinations/australia/overview.html) | Opening image, introduction and education details. | — |
| [settling.html](../templates/partials/destinations/australia/settling.html) | Planning and settling-in advice. | — |
| [work-and-lifestyle.html](../templates/partials/destinations/australia/work-and-lifestyle.html) | Work sectors and student life. | — |
## templates/partials/destinations/canada

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [consultation.html](../templates/partials/destinations/canada/consultation.html) | The closing message and booking link. | — |
| [institutions.html](../templates/partials/destinations/canada/institutions.html) | The university or country list shown on this page. | — |
| [overview.html](../templates/partials/destinations/canada/overview.html) | Opening image, introduction and education details. | — |
| [settling.html](../templates/partials/destinations/canada/settling.html) | Planning and settling-in advice. | — |
| [work-and-lifestyle.html](../templates/partials/destinations/canada/work-and-lifestyle.html) | Work sectors and student life. | — |
## templates/partials/destinations/europe

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [consultation.html](../templates/partials/destinations/europe/consultation.html) | The closing message and booking link. | — |
| [institutions.html](../templates/partials/destinations/europe/institutions.html) | The university or country list shown on this page. | — |
| [overview.html](../templates/partials/destinations/europe/overview.html) | Opening image, introduction and education details. | — |
| [settling.html](../templates/partials/destinations/europe/settling.html) | Planning and settling-in advice. | — |
| [work-and-lifestyle.html](../templates/partials/destinations/europe/work-and-lifestyle.html) | Work sectors and student life. | — |
## templates/partials/destinations/more

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [consultation.html](../templates/partials/destinations/more/consultation.html) | The closing message and booking link. | — |
| [institutions.html](../templates/partials/destinations/more/institutions.html) | The university or country list shown on this page. | — |
| [overview.html](../templates/partials/destinations/more/overview.html) | Opening image, introduction and education details. | — |
| [settling.html](../templates/partials/destinations/more/settling.html) | Planning and settling-in advice. | — |
| [work-and-lifestyle.html](../templates/partials/destinations/more/work-and-lifestyle.html) | Work sectors and student life. | — |
## templates/partials/destinations/uk

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [consultation.html](../templates/partials/destinations/uk/consultation.html) | The closing message and booking link. | — |
| [institutions.html](../templates/partials/destinations/uk/institutions.html) | The university or country list shown on this page. | — |
| [overview.html](../templates/partials/destinations/uk/overview.html) | Opening image, introduction and education details. | — |
| [settling.html](../templates/partials/destinations/uk/settling.html) | Planning and settling-in advice. | — |
| [work-and-lifestyle.html](../templates/partials/destinations/uk/work-and-lifestyle.html) | Work sectors and student life. | — |
## templates/partials/destinations/usa

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [consultation.html](../templates/partials/destinations/usa/consultation.html) | The closing message and booking link. | — |
| [institutions.html](../templates/partials/destinations/usa/institutions.html) | The university or country list shown on this page. | — |
| [overview.html](../templates/partials/destinations/usa/overview.html) | Opening image, introduction and education details. | — |
| [settling.html](../templates/partials/destinations/usa/settling.html) | Planning and settling-in advice. | — |
| [work-and-lifestyle.html](../templates/partials/destinations/usa/work-and-lifestyle.html) | Work sectors and student life. | — |
## templates/partials/home

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [about.html](../templates/partials/home/about.html) | The business introduction. | — |
| [budget-guidance.html](../templates/partials/home/budget-guidance.html) | Study budget advice. | — |
| [consultation.html](../templates/partials/home/consultation.html) | The closing message and booking link. | — |
| [destinations.html](../templates/partials/home/destinations.html) | Destination links and text. | — |
| [hero.html](../templates/partials/home/hero.html) | The homepage opening slides. | — |
| [services.html](../templates/partials/home/services.html) | The study consultancy service section. | — |
| [test-preparation.html](../templates/partials/home/test-preparation.html) | IELTS/PTE information and links. | — |
| [university-showcase.html](../templates/partials/home/university-showcase.html) | The university section on the homepage. | — |
| [why-choose-us.html](../templates/partials/home/why-choose-us.html) | Reasons to choose Visa Culture and supporting images. | — |
## templates/partials/layout

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [contact-widgets.html](../templates/partials/layout/contact-widgets.html) | HTML for the floating booking and WhatsApp buttons. | — |
| [footer.html](../templates/partials/layout/footer.html) | Shared contact details, links, social links and map. | — |
| [mobile-navigation-script.html](../templates/partials/layout/mobile-navigation-script.html) | Adds the phone-menu script to the page. | [scripts/mobile-navigation.js.jinja](../templates/scripts/mobile-navigation.js.jinja) |
| [mobile-navigation.html](../templates/partials/layout/mobile-navigation.html) | The shared phone menu. | — |
| [navigation.html](../templates/partials/layout/navigation.html) | The shared desktop menu. | — |
## templates/partials/preparation/ielts

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [enquiry.html](../templates/partials/preparation/ielts/enquiry.html) | The enquiry message and related page links. | — |
| [practice-and-classes.html](../templates/partials/preparation/ielts/practice-and-classes.html) | Practice, feedback and class details. | — |
| [resources-and-questions.html](../templates/partials/preparation/ielts/resources-and-questions.html) | Official learning links and common questions. | — |
| [test-and-skills.html](../templates/partials/preparation/ielts/test-and-skills.html) | Test choices and skills to practise. | — |
## templates/partials/preparation/pte

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [enquiry.html](../templates/partials/preparation/pte/enquiry.html) | The enquiry message and related page links. | — |
| [practice-and-classes.html](../templates/partials/preparation/pte/practice-and-classes.html) | Practice, feedback and class details. | — |
| [resources-and-questions.html](../templates/partials/preparation/pte/resources-and-questions.html) | Official learning links and common questions. | — |
| [test-and-skills.html](../templates/partials/preparation/pte/test-and-skills.html) | Test choices and skills to practise. | — |
## templates/partials/schema

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [anu_landing-faq.html](../templates/partials/schema/anu_landing-faq.html) | Holds FAQ information for search engines. Keep it the same as the visible answers. | — |
| [melbourne_landing-faq.html](../templates/partials/schema/melbourne_landing-faq.html) | Holds FAQ information for search engines. Keep it the same as the visible answers. | — |
| [sydney_landing-faq.html](../templates/partials/schema/sydney_landing-faq.html) | Holds FAQ information for search engines. Keep it the same as the visible answers. | — |
| [unsw_landing-faq.html](../templates/partials/schema/unsw_landing-faq.html) | Holds FAQ information for search engines. Keep it the same as the visible answers. | — |
| [uq_landing-faq.html](../templates/partials/schema/uq_landing-faq.html) | Holds FAQ information for search engines. Keep it the same as the visible answers. | — |
## templates/partials/universities/anu

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [faq-and-consultation.html](../templates/partials/universities/anu/faq-and-consultation.html) | Questions, answers and booking links. | — |
| [introduction.html](../templates/partials/universities/anu/introduction.html) | Opening text and an overview. | — |
| [student-life-and-process.html](../templates/partials/universities/anu/student-life-and-process.html) | Student life and application steps. | — |
| [study-and-admissions.html](../templates/partials/universities/anu/study-and-admissions.html) | Courses, entry requirements, costs and scholarships. | — |
| [styles.html](../templates/partials/universities/anu/styles.html) | Adds the matching university styles to the page. | [styles/universities/anu/styles.css.jinja](../templates/styles/universities/anu/styles.css.jinja) |
## templates/partials/universities/melbourne

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [faq-and-consultation.html](../templates/partials/universities/melbourne/faq-and-consultation.html) | Questions, answers and booking links. | — |
| [introduction.html](../templates/partials/universities/melbourne/introduction.html) | Opening text and an overview. | — |
| [student-life-and-process.html](../templates/partials/universities/melbourne/student-life-and-process.html) | Student life and application steps. | — |
| [study-and-admissions.html](../templates/partials/universities/melbourne/study-and-admissions.html) | Courses, entry requirements, costs and scholarships. | — |
| [styles-editorial.html](../templates/partials/universities/melbourne/styles-editorial.html) | Adds the matching university styles to the page. | [styles/universities/melbourne/styles-editorial.css.jinja](../templates/styles/universities/melbourne/styles-editorial.css.jinja) |
| [styles.html](../templates/partials/universities/melbourne/styles.html) | Adds the matching university styles to the page. | [styles/universities/melbourne/styles.css.jinja](../templates/styles/universities/melbourne/styles.css.jinja) |
## templates/partials/universities/monash

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [faq-and-consultation.html](../templates/partials/universities/monash/faq-and-consultation.html) | Questions, answers and booking links. | — |
| [introduction.html](../templates/partials/universities/monash/introduction.html) | Opening text and an overview. | — |
| [student-life-and-process.html](../templates/partials/universities/monash/student-life-and-process.html) | Student life and application steps. | — |
| [study-and-admissions.html](../templates/partials/universities/monash/study-and-admissions.html) | Courses, entry requirements, costs and scholarships. | — |
| [styles.html](../templates/partials/universities/monash/styles.html) | Adds the matching university styles to the page. | [styles/universities/monash/styles.css.jinja](../templates/styles/universities/monash/styles.css.jinja) |
## templates/partials/universities/sydney

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [faq-and-consultation.html](../templates/partials/universities/sydney/faq-and-consultation.html) | Questions, answers and booking links. | — |
| [introduction.html](../templates/partials/universities/sydney/introduction.html) | Opening text and an overview. | — |
| [student-life-and-process.html](../templates/partials/universities/sydney/student-life-and-process.html) | Student life and application steps. | — |
| [study-and-admissions.html](../templates/partials/universities/sydney/study-and-admissions.html) | Courses, entry requirements, costs and scholarships. | — |
| [styles.html](../templates/partials/universities/sydney/styles.html) | Adds the matching university styles to the page. | [styles/universities/sydney/styles.css.jinja](../templates/styles/universities/sydney/styles.css.jinja) |

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
## templates/partials/universities/unsw

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [faq-and-consultation.html](../templates/partials/universities/unsw/faq-and-consultation.html) | Questions, answers and booking links. | — |
| [introduction.html](../templates/partials/universities/unsw/introduction.html) | Opening text and an overview. | — |
| [student-life-and-process.html](../templates/partials/universities/unsw/student-life-and-process.html) | Student life and application steps. | — |
| [study-and-admissions.html](../templates/partials/universities/unsw/study-and-admissions.html) | Courses, entry requirements, costs and scholarships. | — |
| [styles.html](../templates/partials/universities/unsw/styles.html) | Adds the matching university styles to the page. | [styles/universities/unsw/styles.css.jinja](../templates/styles/universities/unsw/styles.css.jinja)<br>[styles/universities/unsw/styles-editorial.css.jinja](../templates/styles/universities/unsw/styles-editorial.css.jinja) |
## templates/partials/universities/uq

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [faq-and-consultation.html](../templates/partials/universities/uq/faq-and-consultation.html) | Questions, answers and booking links. | — |
| [introduction.html](../templates/partials/universities/uq/introduction.html) | Opening text and an overview. | — |
| [student-life-and-process.html](../templates/partials/universities/uq/student-life-and-process.html) | Student life and application steps. | — |
| [study-and-admissions.html](../templates/partials/universities/uq/study-and-admissions.html) | Courses, entry requirements, costs and scholarships. | — |
| [styles.html](../templates/partials/universities/uq/styles.html) | Adds the matching university styles to the page. | [styles/universities/uq/styles.css.jinja](../templates/styles/universities/uq/styles.css.jinja) |
## templates

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [pte_preparation.html](../templates/pte_preparation.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[components/preparation.html](../templates/components/preparation.html)<br>[components/preparation.html](../templates/components/preparation.html)<br>[partials/preparation/pte/test-and-skills.html](../templates/partials/preparation/pte/test-and-skills.html)<br>[partials/preparation/pte/practice-and-classes.html](../templates/partials/preparation/pte/practice-and-classes.html)<br>[partials/preparation/pte/resources-and-questions.html](../templates/partials/preparation/pte/resources-and-questions.html)<br>[partials/preparation/pte/enquiry.html](../templates/partials/preparation/pte/enquiry.html) |
## templates/scripts

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [mobile-navigation.js.jinja](../templates/scripts/mobile-navigation.js.jinja) | Controls the phone menu using page links filled in by Python. | — |
## templates/styles/destinations

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [accessibility.css.jinja](../templates/styles/destinations/accessibility.css.jinja) | Sets hidden heading and page-link spacing. Page values can be filled in by Jinja. | — |
| [consultation-foundation.css.jinja](../templates/styles/destinations/consultation-foundation.css.jinja) | Sets consultation section basic styles. Page values can be filled in by Jinja. | — |
| [consultation.css.jinja](../templates/styles/destinations/consultation.css.jinja) | Sets consultation section. Page values can be filled in by Jinja. | — |
| [content-sections.css.jinja](../templates/styles/destinations/content-sections.css.jinja) | Sets page sections sections. Page values can be filled in by Jinja. | — |
| [foundation.css.jinja](../templates/styles/destinations/foundation.css.jinja) | Loads the smaller style files listed here, in order. | [styles/destinations/typography-and-hero.css.jinja](../templates/styles/destinations/typography-and-hero.css.jinja)<br>[styles/destinations/content-sections.css.jinja](../templates/styles/destinations/content-sections.css.jinja)<br>[styles/destinations/network-foundation.css.jinja](../templates/styles/destinations/network-foundation.css.jinja)<br>[styles/destinations/consultation-foundation.css.jinja](../templates/styles/destinations/consultation-foundation.css.jinja)<br>[styles/destinations/responsive-foundation.css.jinja](../templates/styles/destinations/responsive-foundation.css.jinja) |
| [guide.css.jinja](../templates/styles/destinations/guide.css.jinja) | Loads the smaller style files listed here, in order. | [styles/destinations/foundation.css.jinja](../templates/styles/destinations/foundation.css.jinja)<br>[styles/destinations/theme.css.jinja](../templates/styles/destinations/theme.css.jinja)<br>[styles/destinations/layout.css.jinja](../templates/styles/destinations/layout.css.jinja)<br>[styles/destinations/hero.css.jinja](../templates/styles/destinations/hero.css.jinja)<br>[styles/destinations/network.css.jinja](../templates/styles/destinations/network.css.jinja)<br>[styles/destinations/consultation.css.jinja](../templates/styles/destinations/consultation.css.jinja) |
| [hero.css.jinja](../templates/styles/destinations/hero.css.jinja) | Sets opening section. Page values can be filled in by Jinja. | — |
| [layout.css.jinja](../templates/styles/destinations/layout.css.jinja) | Sets layout. Page values can be filled in by Jinja. | — |
| [network-foundation.css.jinja](../templates/styles/destinations/network-foundation.css.jinja) | Sets university list basic styles. Page values can be filled in by Jinja. | — |
| [network.css.jinja](../templates/styles/destinations/network.css.jinja) | Sets university list. Page values can be filled in by Jinja. | — |
| [responsive-foundation.css.jinja](../templates/styles/destinations/responsive-foundation.css.jinja) | Sets phone and tablet sizes basic styles. Page values can be filled in by Jinja. | — |
| [theme.css.jinja](../templates/styles/destinations/theme.css.jinja) | Sets theme. Page values can be filled in by Jinja. | — |
| [typography-and-hero.css.jinja](../templates/styles/destinations/typography-and-hero.css.jinja) | Sets text sizes and fonts and opening section. Page values can be filled in by Jinja. | — |
## templates/styles/universities/anu

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [styles-consultation.css.jinja](../templates/styles/universities/anu/styles-consultation.css.jinja) | Sets consultation section. Page values can be filled in by Jinja. | — |
| [styles-content.css.jinja](../templates/styles/universities/anu/styles-content.css.jinja) | Sets page sections. Page values can be filled in by Jinja. | — |
| [styles-foundation.css.jinja](../templates/styles/universities/anu/styles-foundation.css.jinja) | Sets basic styles. Page values can be filled in by Jinja. | — |
| [styles-hero.css.jinja](../templates/styles/universities/anu/styles-hero.css.jinja) | Sets opening section. Page values can be filled in by Jinja. | — |
| [styles-responsive.css.jinja](../templates/styles/universities/anu/styles-responsive.css.jinja) | Sets phone and tablet sizes. Page values can be filled in by Jinja. | — |
| [styles.css.jinja](../templates/styles/universities/anu/styles.css.jinja) | Loads the smaller style files listed here, in order. | [styles/universities/anu/styles-foundation.css.jinja](../templates/styles/universities/anu/styles-foundation.css.jinja)<br>[styles/universities/anu/styles-hero.css.jinja](../templates/styles/universities/anu/styles-hero.css.jinja)<br>[styles/universities/anu/styles-content.css.jinja](../templates/styles/universities/anu/styles-content.css.jinja)<br>[styles/universities/anu/styles-consultation.css.jinja](../templates/styles/universities/anu/styles-consultation.css.jinja)<br>[styles/universities/anu/styles-responsive.css.jinja](../templates/styles/universities/anu/styles-responsive.css.jinja) |
## templates/styles/universities/melbourne

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [styles-editorial-consultation.css.jinja](../templates/styles/universities/melbourne/styles-editorial-consultation.css.jinja) | Sets page design consultation section. Page values can be filled in by Jinja. | — |
| [styles-editorial-content.css.jinja](../templates/styles/universities/melbourne/styles-editorial-content.css.jinja) | Sets page design page sections. Page values can be filled in by Jinja. | — |
| [styles-editorial-hero.css.jinja](../templates/styles/universities/melbourne/styles-editorial-hero.css.jinja) | Sets page design opening section. Page values can be filled in by Jinja. | — |
| [styles-editorial-responsive.css.jinja](../templates/styles/universities/melbourne/styles-editorial-responsive.css.jinja) | Sets page design phone and tablet sizes. Page values can be filled in by Jinja. | — |
| [styles-editorial.css.jinja](../templates/styles/universities/melbourne/styles-editorial.css.jinja) | Loads the smaller style files listed here, in order. | [styles/universities/melbourne/styles-editorial-hero.css.jinja](../templates/styles/universities/melbourne/styles-editorial-hero.css.jinja)<br>[styles/universities/melbourne/styles-editorial-content.css.jinja](../templates/styles/universities/melbourne/styles-editorial-content.css.jinja)<br>[styles/universities/melbourne/styles-editorial-consultation.css.jinja](../templates/styles/universities/melbourne/styles-editorial-consultation.css.jinja)<br>[styles/universities/melbourne/styles-editorial-responsive.css.jinja](../templates/styles/universities/melbourne/styles-editorial-responsive.css.jinja) |
| [styles.css.jinja](../templates/styles/universities/melbourne/styles.css.jinja) | Sets . Page values can be filled in by Jinja. | — |
## templates/styles/universities/monash

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [styles.css.jinja](../templates/styles/universities/monash/styles.css.jinja) | Sets . Page values can be filled in by Jinja. | — |
## templates/styles/universities/sydney

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [styles-consultation.css.jinja](../templates/styles/universities/sydney/styles-consultation.css.jinja) | Sets consultation section. Page values can be filled in by Jinja. | — |
| [styles-content.css.jinja](../templates/styles/universities/sydney/styles-content.css.jinja) | Sets page sections. Page values can be filled in by Jinja. | — |
| [styles-foundation.css.jinja](../templates/styles/universities/sydney/styles-foundation.css.jinja) | Sets basic styles. Page values can be filled in by Jinja. | — |
| [styles-hero.css.jinja](../templates/styles/universities/sydney/styles-hero.css.jinja) | Sets opening section. Page values can be filled in by Jinja. | — |
| [styles-responsive.css.jinja](../templates/styles/universities/sydney/styles-responsive.css.jinja) | Sets phone and tablet sizes. Page values can be filled in by Jinja. | — |
| [styles.css.jinja](../templates/styles/universities/sydney/styles.css.jinja) | Loads the smaller style files listed here, in order. | [styles/universities/sydney/styles-foundation.css.jinja](../templates/styles/universities/sydney/styles-foundation.css.jinja)<br>[styles/universities/sydney/styles-hero.css.jinja](../templates/styles/universities/sydney/styles-hero.css.jinja)<br>[styles/universities/sydney/styles-content.css.jinja](../templates/styles/universities/sydney/styles-content.css.jinja)<br>[styles/universities/sydney/styles-consultation.css.jinja](../templates/styles/universities/sydney/styles-consultation.css.jinja)<br>[styles/universities/sydney/styles-responsive.css.jinja](../templates/styles/universities/sydney/styles-responsive.css.jinja) |

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
## templates/styles/universities/unsw

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [styles-editorial-consultation.css.jinja](../templates/styles/universities/unsw/styles-editorial-consultation.css.jinja) | Sets page design consultation section. Page values can be filled in by Jinja. | — |
| [styles-editorial-content.css.jinja](../templates/styles/universities/unsw/styles-editorial-content.css.jinja) | Sets page design page sections. Page values can be filled in by Jinja. | — |
| [styles-editorial-foundation.css.jinja](../templates/styles/universities/unsw/styles-editorial-foundation.css.jinja) | Sets page design basic styles. Page values can be filled in by Jinja. | — |
| [styles-editorial-hero.css.jinja](../templates/styles/universities/unsw/styles-editorial-hero.css.jinja) | Sets page design opening section. Page values can be filled in by Jinja. | — |
| [styles-editorial-responsive.css.jinja](../templates/styles/universities/unsw/styles-editorial-responsive.css.jinja) | Sets page design phone and tablet sizes. Page values can be filled in by Jinja. | — |
| [styles-editorial.css.jinja](../templates/styles/universities/unsw/styles-editorial.css.jinja) | Loads the smaller style files listed here, in order. | [styles/universities/unsw/styles-editorial-foundation.css.jinja](../templates/styles/universities/unsw/styles-editorial-foundation.css.jinja)<br>[styles/universities/unsw/styles-editorial-hero.css.jinja](../templates/styles/universities/unsw/styles-editorial-hero.css.jinja)<br>[styles/universities/unsw/styles-editorial-content.css.jinja](../templates/styles/universities/unsw/styles-editorial-content.css.jinja)<br>[styles/universities/unsw/styles-editorial-consultation.css.jinja](../templates/styles/universities/unsw/styles-editorial-consultation.css.jinja)<br>[styles/universities/unsw/styles-editorial-responsive.css.jinja](../templates/styles/universities/unsw/styles-editorial-responsive.css.jinja) |
| [styles.css.jinja](../templates/styles/universities/unsw/styles.css.jinja) | Sets . Page values can be filled in by Jinja. | — |
## templates/styles/universities/uq

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [styles.css.jinja](../templates/styles/universities/uq/styles.css.jinja) | Sets . Page values can be filled in by Jinja. | — |
## templates

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [sydney_landing.html](../templates/sydney_landing.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[partials/universities/sydney/styles.html](../templates/partials/universities/sydney/styles.html)<br>[partials/schema/sydney_landing-faq.html](../templates/partials/schema/sydney_landing-faq.html)<br>[partials/universities/sydney/introduction.html](../templates/partials/universities/sydney/introduction.html)<br>[partials/universities/sydney/study-and-admissions.html](../templates/partials/universities/sydney/study-and-admissions.html)<br>[partials/universities/sydney/student-life-and-process.html](../templates/partials/universities/sydney/student-life-and-process.html)<br>[partials/universities/sydney/faq-and-consultation.html](../templates/partials/universities/sydney/faq-and-consultation.html) |
| [uk.html](../templates/uk.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[_destination_guide_styles.html](../templates/_destination_guide_styles.html)<br>[styles/destinations/accessibility.css.jinja](../templates/styles/destinations/accessibility.css.jinja)<br>[partials/destinations/uk/overview.html](../templates/partials/destinations/uk/overview.html)<br>[partials/destinations/uk/work-and-lifestyle.html](../templates/partials/destinations/uk/work-and-lifestyle.html)<br>[partials/destinations/uk/settling.html](../templates/partials/destinations/uk/settling.html)<br>[partials/destinations/uk/institutions.html](../templates/partials/destinations/uk/institutions.html)<br>[partials/destinations/uk/consultation.html](../templates/partials/destinations/uk/consultation.html) |
| [unsw_landing.html](../templates/unsw_landing.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[partials/universities/unsw/styles.html](../templates/partials/universities/unsw/styles.html)<br>[partials/schema/unsw_landing-faq.html](../templates/partials/schema/unsw_landing-faq.html)<br>[partials/universities/unsw/introduction.html](../templates/partials/universities/unsw/introduction.html)<br>[partials/universities/unsw/study-and-admissions.html](../templates/partials/universities/unsw/study-and-admissions.html)<br>[partials/universities/unsw/student-life-and-process.html](../templates/partials/universities/unsw/student-life-and-process.html)<br>[partials/universities/unsw/faq-and-consultation.html](../templates/partials/universities/unsw/faq-and-consultation.html) |
| [uq_landing.html](../templates/uq_landing.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[partials/universities/uq/styles.html](../templates/partials/universities/uq/styles.html)<br>[partials/schema/uq_landing-faq.html](../templates/partials/schema/uq_landing-faq.html)<br>[partials/universities/uq/introduction.html](../templates/partials/universities/uq/introduction.html)<br>[partials/universities/uq/study-and-admissions.html](../templates/partials/universities/uq/study-and-admissions.html)<br>[partials/universities/uq/student-life-and-process.html](../templates/partials/universities/uq/student-life-and-process.html)<br>[partials/universities/uq/faq-and-consultation.html](../templates/partials/universities/uq/faq-and-consultation.html) |
| [usa.html](../templates/usa.html) | Sets this page’s title, search description and section order. | [base.html](../templates/base.html)<br>[_destination_guide_styles.html](../templates/_destination_guide_styles.html)<br>[styles/destinations/accessibility.css.jinja](../templates/styles/destinations/accessibility.css.jinja)<br>[partials/destinations/usa/overview.html](../templates/partials/destinations/usa/overview.html)<br>[partials/destinations/usa/work-and-lifestyle.html](../templates/partials/destinations/usa/work-and-lifestyle.html)<br>[partials/destinations/usa/settling.html](../templates/partials/destinations/usa/settling.html)<br>[partials/destinations/usa/institutions.html](../templates/partials/destinations/usa/institutions.html)<br>[partials/destinations/usa/consultation.html](../templates/partials/destinations/usa/consultation.html) |
## tests

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [__init__.py](../tests/__init__.py) | Marks the tests folder as a Python package. | — |
| [browser_check.py](../tests/browser_check.py) | Compares desktop and phone pages with the older version. | `main()` |
| [contracts.py](../tests/contracts.py) | Helps checks compare page output, style rules and moved files. | `expand_css()`<br>`normalized_body()`<br>`components()`<br>`css_contract()`<br>`canonical_body()` |
## tests/fixtures

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [behavior.json](../tests/fixtures/behavior.json) | Stores expected page links, page results, emails and spam-check results. | — |
| [extracted_assets.json](../tests/fixtures/extracted_assets.json) | Lists files moved out of HTML so the checks can compare them. | — |
| [reference.json](../tests/fixtures/reference.json) | Names the older Git version used for browser checks. | — |
| [scripts.json](../tests/fixtures/scripts.json) | Stores checksums used to spot changes to scripts. | — |
| [styles.json](../tests/fixtures/styles.json) | Stores checksums used to spot changes to style rules. | — |
## tests

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [reference_app.py](../tests/reference_app.py) | Reads an older app version from Git for browser comparisons. | `load_reference()` |
| [test_regression.py](../tests/test_regression.py) | Checks that pages, forms, emails, scripts and styles still work as expected. | `response_snapshot()`<br>`capture()` |
| [test_seo.py](../tests/test_seo.py) | Checks page search details, search data and local contact links. | — |
## tools

| File | What it does | Files it loads or functions to find |
| --- | --- | --- |
| [format_styles.py](../tools/format_styles.py) | Tidies spacing in CSS files without changing rule order. | `declarations()`<br>`rules()`<br>`format_style()`<br>`main()` |

## Images

Images are stored in `static/images/`. Some have separate desktop and phone versions. Keep filenames, spaces and letter case correct when replacing images. A file that works on Windows can still fail online if its letter case is wrong.

To find where an image is used, replace `filename.webp` in this command:

```powershell
rg -n -F "filename.webp" templates backend static/css
```

## Keep this list up to date

When a file is added, moved or removed, update its row here. Update the [project guide](DEVELOPER_MAP.md) too if the way the website works has changed.
