(function() {
    'use strict';

    let searchTimeout;
    const DEBOUNCE_DELAY = 300;
    const MIN_QUERY_LENGTH = 2;

    const searchInput = document.querySelector('.search-input');
    const searchForm = document.querySelector('.search-form');
    const suggestionsContainer = document.querySelector('.search-suggestions');

    if (!searchInput || !searchForm) {
        return;
    }

    if (!suggestionsContainer) {
        const container = document.createElement('div');
        container.className = 'search-suggestions';
        searchForm.appendChild(container);
    }

    function performSearch(query) {
        if (query.length < MIN_QUERY_LENGTH) {
            hideSuggestions();
            return;
        }

        const url = `/api/search/?q=${encodeURIComponent(query)}`;

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displaySuggestions(data.results);
            } else {
                hideSuggestions();
            }
        })
        .catch(error => {
            console.error('Search error:', error);
            hideSuggestions();
        });
    }

    function displaySuggestions(results) {
        const container = document.querySelector('.search-suggestions');
        if (!container) return;

        if (results.length === 0) {
            container.innerHTML = '<div class="suggestion-item suggestion-empty">Ничего не найдено</div>';
            container.style.display = 'block';
            return;
        }

        let html = '';
        results.forEach(result => {
            html += `
                <a href="${result.url}" class="suggestion-item">
                    <div class="suggestion-title">${escapeHtml(result.title)}</div>
                    <div class="suggestion-text">${escapeHtml(result.text)}</div>
                    <div class="suggestion-meta">
                        <span class="suggestion-author">${escapeHtml(result.author)}</span>
                        <span class="suggestion-score">Score: ${result.score}</span>
                    </div>
                </a>
            `;
        });

        container.innerHTML = html;
        container.style.display = 'block';
    }

    function hideSuggestions() {
        const container = document.querySelector('.search-suggestions');
        if (container) {
            container.style.display = 'none';
        }
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.trim();

        clearTimeout(searchTimeout);

        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, DEBOUNCE_DELAY);
    });

    searchInput.addEventListener('focus', function(e) {
        const query = e.target.value.trim();
        if (query.length >= MIN_QUERY_LENGTH) {
            performSearch(query);
        }
    });

    document.addEventListener('click', function(e) {
        if (!searchForm.contains(e.target)) {
            hideSuggestions();
        }
    });

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const query = searchInput.value.trim();
        if (query.length >= MIN_QUERY_LENGTH) {
            window.location.href = `/?filter=search&q=${encodeURIComponent(query)}`;
        }
    });

    searchInput.addEventListener('keydown', function(e) {
        const container = document.querySelector('.search-suggestions');
        if (!container || container.style.display === 'none') {
            return;
        }

        const items = container.querySelectorAll('.suggestion-item');
        if (items.length === 0) return;

        let currentIndex = -1;
        items.forEach((item, index) => {
            if (item.classList.contains('suggestion-active')) {
                currentIndex = index;
            }
        });

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            items.forEach(item => item.classList.remove('suggestion-active'));
            const nextIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
            items[nextIndex].classList.add('suggestion-active');
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            items.forEach(item => item.classList.remove('suggestion-active'));
            const prevIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
            items[prevIndex].classList.add('suggestion-active');
        } else if (e.key === 'Enter') {
            const activeItem = container.querySelector('.suggestion-item.suggestion-active');
            if (activeItem && activeItem.href) {
                e.preventDefault();
                window.location.href = activeItem.href;
            }
        } else if (e.key === 'Escape') {
            hideSuggestions();
        }
    });
})();
