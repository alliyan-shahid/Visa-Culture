        document.addEventListener('DOMContentLoaded', function() {
            const viewMoreBtn = document.getElementById('viewMoreBtn');
            const collapsibleContent = document.getElementById('collapsibleContent');
            if (viewMoreBtn && collapsibleContent) {
                viewMoreBtn.addEventListener('click', function() {
                    collapsibleContent.classList.toggle('expanded');
                    viewMoreBtn.classList.toggle('expanded');
                    viewMoreBtn.querySelector('.btn-text').textContent = collapsibleContent.classList.contains('expanded') ? 'View Less Details' : 'View More Details';
                });
            }
        });
    