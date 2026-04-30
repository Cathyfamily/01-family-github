document.addEventListener('DOMContentLoaded', () => {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Simple Tab Switching Logic
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked
            btn.classList.add('active');
            const targetId = btn.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
            
            // Optional: Update URL without reloading to persist state
            const url = new URL(window.location);
            url.searchParams.set('tab', targetId);
            window.history.pushState({}, '', url);
        });
    });

    // Check URL params for active tab on load
    const urlParams = new URLSearchParams(window.location.search);
    const activeTab = urlParams.get('tab');
    if (activeTab) {
        const targetBtn = document.querySelector(`.tab-btn[data-target="${activeTab}"]`);
        if (targetBtn) {
            targetBtn.click();
        }
    }

    // --- Sorting Logic ---
    function sortElements(containerId, itemClass, sortKey, sortOrder, isDate = false) {
        const container = document.getElementById(containerId);
        if (!container) return;
        const items = Array.from(container.querySelectorAll(`.${itemClass}`));

        items.sort((a, b) => {
            let valA = a.getAttribute(`data-${sortKey}`);
            let valB = b.getAttribute(`data-${sortKey}`);
            
            if (isDate) {
                valA = new Date(valA || 0).getTime();
                valB = new Date(valB || 0).getTime();
            } else {
                valA = valA ? valA.toLowerCase() : '';
                valB = valB ? valB.toLowerCase() : '';
            }

            if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
            if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
            return 0;
        });

        items.forEach(item => container.appendChild(item));
    }

    const sortStocks = document.getElementById('sort-stocks');
    if (sortStocks) {
        sortStocks.addEventListener('change', (e) => {
            const [key, order] = e.target.value.split('-');
            sortElements('stocks-tbody', 'stock-item', key, order, true);
        });
    }

    const sortMilestones = document.getElementById('sort-milestones');
    if (sortMilestones) {
        sortMilestones.addEventListener('change', (e) => {
            const [key, order] = e.target.value.split('-');
            sortElements('milestones-grid', 'milestone-item', key, order, true);
        });
    }

    const sortRecipes = document.getElementById('sort-recipes');
    if (sortRecipes) {
        sortRecipes.addEventListener('change', (e) => {
            const [key, order] = e.target.value.split('-');
            const isDate = key === 'time';
            sortElements('recipes-grid', 'recipe-item', key, order, isDate);
        });
    }
});
