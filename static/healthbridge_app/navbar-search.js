// Navbar Medicine Autocomplete
// Handles the search functionality in the navigation bar

(function() {
  const input = document.getElementById('navbar-search-input');
  if (!input) return; // Exit if not on authenticated pages
  
  const container = document.getElementById('navbar-autocomplete-suggestions');
  let debounceTimer = null;
  let selectedIndex = -1;
  let suggestions = [];

  // Show loading state
  function showLoading() {
    container.innerHTML = '<div class="navbar-autocomplete-loading">🔍 Searching medicines...</div>';
    container.classList.add('show');
  }

  // Show empty state
  function showEmpty() {
    container.innerHTML = '<div class="navbar-autocomplete-empty">❌ No medicines found</div>';
    container.classList.add('show');
  }

  // Hide suggestions
  function hide() {
    container.classList.remove('show');
    selectedIndex = -1;
  }

  // Escape HTML to prevent XSS
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Highlight matching text
  function highlightMatch(text, query) {
    const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    return text.replace(regex, '<strong>$1</strong>');
  }

  // Display suggestions
  function display(query) {
    if (suggestions.length === 0) {
      showEmpty();
      return;
    }

    const html = suggestions.map((suggestion, index) => {
      const highlighted = highlightMatch(escapeHtml(suggestion), escapeHtml(query));
      return `
        <div class="navbar-autocomplete-item" data-index="${index}" data-value="${escapeHtml(suggestion)}">
          <span class="navbar-autocomplete-icon">💊</span>
          <span>${highlighted}</span>
        </div>
      `;
    }).join('');

    container.innerHTML = html;
    container.classList.add('show');

    // Add click handlers to each suggestion
    container.querySelectorAll('.navbar-autocomplete-item').forEach(item => {
      item.addEventListener('click', () => {
        input.value = item.dataset.value;
        hide();
        input.form.submit();
      });
    });
  }

  // Fetch suggestions from API
  async function fetchSuggestions(query) {
    if (!query || query.length < 2) {
      hide();
      return;
    }

    showLoading();

    try {
      const response = await fetch(`/donations/api/autocomplete/?q=${encodeURIComponent(query)}`);
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      suggestions = data.suggestions || [];
      display(query);
    } catch (error) {
      console.error('Autocomplete error:', error);
      container.innerHTML = '<div class="navbar-autocomplete-empty">⚠️ Error loading suggestions</div>';
      container.classList.add('show');
    }
  }

  // Handle input changes with debouncing
  input.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => fetchSuggestions(query), 300);
  });

  // Show suggestions on focus if query exists
  input.addEventListener('focus', () => {
    const query = input.value.trim();
    if (query.length >= 2 && suggestions.length > 0) {
      container.classList.add('show');
    }
  });

  // Keyboard navigation
  input.addEventListener('keydown', (e) => {
    const items = container.querySelectorAll('.navbar-autocomplete-item');
    
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
      updateSelection(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIndex = Math.max(selectedIndex - 1, -1);
      updateSelection(items);
    } else if (e.key === 'Enter') {
      if (selectedIndex >= 0 && items.length > 0) {
        e.preventDefault();
        items[selectedIndex].click();
      }
      // Otherwise let form submit naturally
    } else if (e.key === 'Escape') {
      hide();
      input.blur();
    }
  });

  // Update visual selection
  function updateSelection(items) {
    items.forEach((item, index) => {
      if (index === selectedIndex) {
        item.classList.add('selected');
        item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      } else {
        item.classList.remove('selected');
      }
    });
  }

  // Close suggestions on outside click
  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !container.contains(e.target)) {
      hide();
    }
  });

  // Clear search on escape when no suggestions
  input.addEventListener('keyup', (e) => {
    if (e.key === 'Escape' && !container.classList.contains('show')) {
      input.value = '';
    }
  });
})();
