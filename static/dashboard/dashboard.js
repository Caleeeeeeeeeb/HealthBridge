// Dashboard JavaScript - HealthBridge
// Modal and AJAX form handling

// Modal Functions
function openDonateModal() {
  document.getElementById('donateModal').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeDonateModal() {
  document.getElementById('donateModal').classList.remove('active');
  document.body.style.overflow = '';
  document.getElementById('donateForm').reset();
}

function openRequestModal() {
  document.getElementById('requestModal').classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeRequestModal() {
  document.getElementById('requestModal').classList.remove('active');
  document.body.style.overflow = '';
  document.getElementById('requestForm').reset();
}

// Close modal on outside click
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', function(e) {
      if (e.target === this) {
        closeDonateModal();
        closeRequestModal();
      }
    });
  });

  // Initialize AJAX form handlers
  initDonateForm();
  initRequestForm();
});

// AJAX Form Submission - Donate
function initDonateForm() {
  const donateForm = document.getElementById('donateForm');
  if (!donateForm) return;

  donateForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>⏳</span> Submitting...';
    
    try {
      // Get URL from data attribute set in template
      const url = donateForm.dataset.submitUrl;
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      
      if (response.ok) {
        closeDonateModal();
        showToast('✅ Medicine donated successfully! Reloading page...', 'success');
        setTimeout(() => window.location.reload(), 1500);
      } else {
        showToast('❌ Error submitting donation. Please try again.', 'error');
      }
    } catch (error) {
      showToast('❌ Network error. Please check your connection.', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    }
  });
}

// AJAX Form Submission - Request
function initRequestForm() {
  const requestForm = document.getElementById('requestForm');
  if (!requestForm) return;

  requestForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>⏳</span> Submitting...';
    
    try {
      // Get URL from data attribute set in template
      const url = requestForm.dataset.submitUrl;
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
      
      if (response.ok) {
        closeRequestModal();
        showToast('✅ Medicine request submitted successfully! Reloading page...', 'success');
        setTimeout(() => window.location.reload(), 1500);
      } else {
        showToast('❌ Error submitting request. Please try again.', 'error');
      }
    } catch (error) {
      showToast('❌ Network error. Please check your connection.', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    }
  });
}

// Toast Notification Function
function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    max-width: 400px;
    padding: 1rem 1.5rem;
    background: ${type === 'error' ? '#f87171' : '#4ade80'};
    color: white;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    font-weight: 600;
    animation: slideIn 0.3s ease;
  `;
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(400px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
