// Admin Dashboard JavaScript

// Get today's date for the date picker
const today = new Date().toISOString().split('T')[0];

function showModal(modalId) {
    document.getElementById(modalId).classList.add('show');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

function approveDonation(donationId) {
    if (confirm('Are you sure you want to approve this donation?')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin-dashboard/approve-donation/${donationId}/`;
        
        const csrf = document.createElement('input');
        csrf.type = 'hidden';
        csrf.name = 'csrfmiddlewaretoken';
        csrf.value = getCookie('csrftoken');
        form.appendChild(csrf);
        
        document.body.appendChild(form);
        form.submit();
    }
}

function showRejectDonationModal(donationId, name) {
    const form = document.getElementById('rejectDonationForm');
    form.action = `/admin-dashboard/reject-donation/${donationId}/`;
    showModal('rejectDonationModal');
}

function showApproveRequestModal(requestId, name) {
    const form = document.getElementById('approveRequestForm');
    form.action = `/admin-dashboard/approve-request/${requestId}/`;
    showModal('approveRequestModal');
}

function showRejectRequestModal(requestId, name) {
    const form = document.getElementById('rejectRequestForm');
    form.action = `/admin-dashboard/reject-request/${requestId}/`;
    showModal('rejectRequestModal');
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Close modals on background click
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('show');
            }
        });
    });

    // Auto-hide messages after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            alert.style.animation = 'slideOut 0.3s forwards';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
});
