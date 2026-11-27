"""Published sitemap paths and priorities, in their existing order."""


def get_sitemap_pages():
    pages = [
        {"path": "", "priority": 1.0},
        {"path": "australia", "priority": 0.9},
        {"path": "usa", "priority": 0.9},
        {"path": "uk", "priority": 0.9},
        {"path": "canada", "priority": 0.9},
        {"path": "europe", "priority": 0.9},
        {"path": "more", "priority": 0.9},
        {"path": "booking", "priority": 0.7},
        {"path": "ielts-preparation", "priority": 0.7},
        {"path": "pte-preparation", "priority": 0.7},
    ]
    university_pages = [
        {"path": "australia/university-of-melbourne", "priority": 0.9},
        {"path": "australia/australian-national-university", "priority": 0.9},
        {"path": "australia/university-of-sydney", "priority": 0.9},
        {"path": "australia/unsw-sydney", "priority": 0.9},
        {"path": "australia/monash-university", "priority": 0.9},
        {"path": "australia/university-of-queensland", "priority": 0.9},
    ]

    return pages + university_pages
