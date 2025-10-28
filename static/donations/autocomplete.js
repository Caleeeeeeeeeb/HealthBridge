// Medicine Autocomplete Component
// Reusable autocomplete functionality for medicine search

class MedicineAutocomplete {
  constructor(inputElement, options = {}) {
    this.input = inputElement;
    this.container = null;
    this.suggestions = [];
    this.selectedIndex = -1;
    this.debounceTimer = null;
    
    // Options
    this.minChars = options.minChars || 2;
    this.debounceDelay = options.debounceDelay || 500; // Increased to 500ms for slower connections
    this.apiUrl = options.apiUrl || '/api/medicine-autocomplete/';
    this.onSelect = options.onSelect || null;
    
    this.init();
  }

  init() {
    // Create suggestions container
    this.createContainer();
    
    // Add event listeners
    this.input.addEventListener('input', (e) => this.handleInput(e));
    this.input.addEventListener('keydown', (e) => this.handleKeyDown(e));
    this.input.addEventListener('focus', () => this.handleFocus());
    
    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!this.input.contains(e.target) && !this.container.contains(e.target)) {
        this.hide();
      }
    });
  }

  createContainer() {
    // Wrap input in relative container if not already wrapped
    if (!this.input.parentElement.classList.contains('autocomplete-wrapper')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'autocomplete-wrapper';
      wrapper.style.position = 'relative';
      this.input.parentNode.insertBefore(wrapper, this.input);
      wrapper.appendChild(this.input);
    }

    // Create suggestions container
    this.container = document.createElement('div');
    this.container.className = 'autocomplete-suggestions';
    this.input.parentElement.appendChild(this.container);
  }

  handleInput(e) {
    const query = e.target.value.trim();
    
    clearTimeout(this.debounceTimer);
    this.debounceTimer = setTimeout(() => {
      this.fetchSuggestions(query);
    }, this.debounceDelay);
  }

  handleFocus() {
    const query = this.input.value.trim();
    if (query.length >= this.minChars) {
      this.fetchSuggestions(query);
    }
  }

  async fetchSuggestions(query) {
    if (!query || query.length < this.minChars) {
      this.hide();
      return;
    }

    this.showLoading();

    try {
      const response = await fetch(`${this.apiUrl}?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      this.suggestions = data.suggestions || [];
      this.display(query);
    } catch (error) {
      console.error('Autocomplete error:', error);
      this.hide();
    }
  }

  display(query) {
    if (this.suggestions.length === 0) {
      this.showEmpty();
      return;
    }

    const queryLower = query.toLowerCase();
    const html = this.suggestions.map((suggestion, index) => {
      const highlighted = this.highlightMatch(suggestion, query);
      return `
        <div class="autocomplete-item" data-index="${index}" data-value="${this.escapeHtml(suggestion)}">
          <span class="autocomplete-icon">💊</span>
          <span class="autocomplete-text">${highlighted}</span>
        </div>
      `;
    }).join('');

    this.container.innerHTML = html;
    this.container.classList.add('active');
    this.selectedIndex = -1;

    // Add click handlers
    this.container.querySelectorAll('.autocomplete-item').forEach(item => {
      item.addEventListener('click', () => this.select(item.dataset.value));
    });
  }

  highlightMatch(text, query) {
    const index = text.toLowerCase().indexOf(query.toLowerCase());
    if (index === -1) return this.escapeHtml(text);

    const before = this.escapeHtml(text.substring(0, index));
    const match = this.escapeHtml(text.substring(index, index + query.length));
    const after = this.escapeHtml(text.substring(index + query.length));

    return `${before}<strong>${match}</strong>${after}`;
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  showLoading() {
    this.container.innerHTML = '<div class="autocomplete-loading">🔍 Searching...</div>';
    this.container.classList.add('active');
  }

  showEmpty() {
    this.container.innerHTML = '<div class="autocomplete-empty">No medicines found</div>';
    this.container.classList.add('active');
  }

  hide() {
    this.container.classList.remove('active');
    this.selectedIndex = -1;
  }

  select(value) {
    this.input.value = value;
    this.hide();
    this.input.focus();
    
    if (this.onSelect) {
      this.onSelect(value);
    }
  }

  handleKeyDown(e) {
    if (!this.container.classList.contains('active')) return;

    const items = this.container.querySelectorAll('.autocomplete-item');
    if (items.length === 0) return;

    switch(e.key) {
      case 'ArrowDown':
        e.preventDefault();
        this.selectedIndex = Math.min(this.selectedIndex + 1, items.length - 1);
        this.updateSelection(items);
        break;
      case 'ArrowUp':
        e.preventDefault();
        this.selectedIndex = Math.max(this.selectedIndex - 1, -1);
        this.updateSelection(items);
        break;
      case 'Enter':
        if (this.selectedIndex >= 0) {
          e.preventDefault();
          this.select(items[this.selectedIndex].dataset.value);
        }
        break;
      case 'Escape':
        e.preventDefault();
        this.hide();
        break;
    }
  }

  updateSelection(items) {
    items.forEach((item, index) => {
      item.classList.toggle('selected', index === this.selectedIndex);
    });

    if (this.selectedIndex >= 0 && items[this.selectedIndex]) {
      items[this.selectedIndex].scrollIntoView({ block: 'nearest' });
    }
  }
}

// Auto-initialize on elements with data-autocomplete attribute
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-autocomplete="medicine"]').forEach(input => {
    new MedicineAutocomplete(input);
  });
});
