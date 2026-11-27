"""Destination content. Builders return fresh collections for each request."""


def get_usa_universities():
    return [
            {
                "id": "mit",
                "name": "Massachusetts Institute of Technology (MIT)",
                "category": "Private research university",
                "region": "Cambridge, Massachusetts",
                "summary": "Explore engineering, computing and the sciences, with hands-on research through MIT's Undergraduate Research Opportunities Program.",
                "url": "https://www.mit.edu/",
            },
            {
                "id": "stanford",
                "name": "Stanford University",
                "category": "Private research university",
                "region": "Stanford, California",
                "summary": "Explore engineering, computer science, humanities and interdisciplinary study in Silicon Valley.",
                "url": "https://www.stanford.edu/",
            },
            {
                "id": "harvard",
                "name": "Harvard University",
                "category": "Private research university",
                "region": "Cambridge, Massachusetts",
                "summary": "Harvard College offers a liberal arts and sciences education with concentrations across the humanities, social sciences and natural sciences.",
                "url": "https://www.harvard.edu/",
            },
            {
                "id": "caltech",
                "name": "California Institute of Technology (Caltech)",
                "category": "Private research university",
                "region": "Pasadena, California",
                "summary": "A small institution focused on science and engineering, with undergraduate research opportunities in areas such as physics and aerospace.",
                "url": "https://www.caltech.edu/",
            },
            {
                "id": "princeton",
                "name": "Princeton University",
                "category": "Private research university",
                "region": "Princeton, New Jersey",
                "summary": "Explore liberal arts and engineering programs that emphasize independent work, including junior projects and senior theses.",
                "url": "https://www.princeton.edu/",
            },
            {
                "id": "berkeley",
                "name": "University of California, Berkeley",
                "category": "Public research university",
                "region": "Berkeley, California",
                "summary": "A University of California campus offering programs across engineering, computing, business, the sciences and the liberal arts.",
                "url": "https://www.berkeley.edu/",
            },
        ]


def get_uk_universities():
    return [
            {
                "id": "oxford",
                "name": "University of Oxford",
                "category": "Collegiate university",
                "region": "Oxford, England",
                "summary": "Explore humanities, sciences and social sciences in a collegiate system where undergraduate tutorials are central to teaching.",
                "url": "https://www.ox.ac.uk/",
            },
            {
                "id": "cambridge",
                "name": "University of Cambridge",
                "category": "Collegiate university",
                "region": "Cambridge, England",
                "summary": "Choose from arts, sciences and engineering, with small-group undergraduate teaching known as supervisions.",
                "url": "https://www.cam.ac.uk/",
            },
            {
                "id": "imperial",
                "name": "Imperial College London",
                "category": "Specialist research university",
                "region": "London, England",
                "summary": "Study science, engineering, medicine or business at a university with a strong focus on applied research.",
                "url": "https://www.imperial.ac.uk/",
            },
            {
                "id": "ucl",
                "name": "University College London (UCL)",
                "category": "Research university",
                "region": "London, England",
                "summary": "Explore architecture, education, health sciences, engineering and the humanities at a university based in central London.",
                "url": "https://www.ucl.ac.uk/",
            },
            {
                "id": "edinburgh",
                "name": "University of Edinburgh",
                "category": "Research university",
                "region": "Edinburgh, Scotland",
                "summary": "Explore subjects from informatics and medicine to literature and social sciences in Scotland’s capital.",
                "url": "https://www.ed.ac.uk/",
            },
            {
                "id": "manchester",
                "name": "University of Manchester",
                "category": "Research university",
                "region": "Manchester, England",
                "summary": "Choose from engineering, science, business and humanities programmes at a large university in northern England.",
                "url": "https://www.manchester.ac.uk/",
            },
        ]


def get_canada_universities():
    return [
            {
                "id": "toronto",
                "name": "University of Toronto",
                "category": "Research university",
                "region": "Greater Toronto Area, Ontario",
                "summary": "Explore programs in computing, engineering, health sciences, humanities and social sciences across three campuses.",
                "url": "https://www.utoronto.ca/",
            },
            {
                "id": "ubc",
                "name": "University of British Columbia (UBC)",
                "category": "Research university",
                "region": "Vancouver and Kelowna, British Columbia",
                "summary": "Compare programs in science, forestry, engineering and business at the Vancouver and Okanagan campuses.",
                "url": "https://www.ubc.ca/",
            },
            {
                "id": "mcgill",
                "name": "McGill University",
                "category": "Research university",
                "region": "Montréal, Québec",
                "summary": "Explore programs in life sciences, engineering, management and the arts in an English-language university in Montréal.",
                "url": "https://www.mcgill.ca/",
            },
            {
                "id": "waterloo",
                "name": "University of Waterloo",
                "category": "Research university",
                "region": "Waterloo, Ontario",
                "summary": "Explore mathematics, computer science and engineering, with co-op options in many undergraduate programs.",
                "url": "https://uwaterloo.ca/",
            },
            {
                "id": "alberta",
                "name": "University of Alberta",
                "category": "Research university",
                "region": "Edmonton, Alberta",
                "summary": "Compare programs in engineering, computing, agriculture, health sciences and the humanities.",
                "url": "https://www.ualberta.ca/",
            },
            {
                "id": "mcmaster",
                "name": "McMaster University",
                "category": "Research university",
                "region": "Hamilton, Ontario",
                "summary": "Explore health sciences, engineering, business and the humanities, including programs with inquiry-based learning.",
                "url": "https://www.mcmaster.ca/",
            },
        ]


def get_europe_countries():
    return [
            {
                "id": "germany",
                "name": "Germany",
                "summary": "Compare research universities and universities of applied sciences. Many public programmes have low tuition, with exceptions by state, institution and course.",
                "url": "https://www.study-in-germany.de/en/",
            },
            {
                "id": "france",
                "name": "France",
                "summary": "Explore public universities, grandes écoles and specialist schools. Compare French- and English-taught programmes and check which international fees apply.",
                "url": "https://www.campusfrance.org/en",
            },
            {
                "id": "hungary",
                "name": "Hungary",
                "summary": "Explore programmes taught in English and check whether you qualify for the Stipendium Hungaricum scholarship.",
                "url": "https://education.ec.europa.eu/study-in-europe/country-profiles/hungary",
            },
            {
                "id": "italy",
                "name": "Italy",
                "summary": "Explore programmes in design, architecture, engineering, sciences and the humanities. Compare tuition and regional scholarships.",
                "url": "https://www.universitaly.it/",
            },
            {
                "id": "sweden",
                "name": "Sweden",
                "summary": "Explore English-taught programmes in fields such as sustainability, engineering and design. Compare university and national scholarship eligibility.",
                "url": "https://studyinsweden.se/",
            },
            {
                "id": "netherlands",
                "name": "Netherlands",
                "summary": "Compare English-taught programmes at research universities and universities of applied sciences. Check tuition and start looking for housing early.",
                "url": "https://www.studyinnl.org/",
            },
        ]


def get_more_countries():
    return [
            {
                "id": "japan",
                "name": "Japan",
                "summary": "Compare Japanese- and English-taught degrees in engineering, robotics, design and other fields. Check MEXT and university scholarship options.",
                "url": "https://www.studyinjapan.go.jp/en/planning/",
            },
            {
                "id": "singapore",
                "name": "Singapore",
                "summary": "Explore computing, engineering, business and life sciences. Compare entry requirements and check the terms of any tuition grant before accepting it.",
                "url": "https://www.ica.gov.sg/information-and-e-services/long-term-visit-and-study/student-s-pass/student%27s-pass-application-renewal/institutes-of-higher-learning",
            },
            {
                "id": "uae",
                "name": "United Arab Emirates (UAE)",
                "summary": "Compare local universities and international branch campuses. Check accreditation for your exact programme and ask about student residence sponsorship.",
                "url": "https://u.ae/en/information-and-services/education/higher-education/Student-admission-and-qualification-recognition",
            },
            {
                "id": "malaysia",
                "name": "Malaysia",
                "summary": "Compare local universities and international branch campuses with English-taught options in computing, business and engineering.",
                "url": "https://studymalaysia.com/",
            },
            {
                "id": "ireland",
                "name": "Ireland",
                "summary": "Explore English-taught programmes in technology, business and life sciences. Budget for housing and check which graduate options apply to your degree.",
                "url": "https://www.educationinireland.com/en/plan-your-study-abroad",
            },
            {
                "id": "south-korea",
                "name": "South Korea",
                "summary": "Compare Korean- and English-taught programmes in engineering, computing, business and design. Check Global Korea Scholarship eligibility.",
                "url": "https://www.studyinkorea.go.kr/en/plan/main.do",
            },
        ]
