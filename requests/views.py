from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import MedicineRequest
from donations.models import Donation


@login_required
def request_medicine(request):
    """Allow recipients to request medicines"""
    
    # Pre-fill data from URL parameters (when coming from search page)
    prefill_data = {
        'medicine_name': request.GET.get('medicine', ''),
        'quantity': request.GET.get('quantity', ''),
        'donor_name': request.GET.get('donor', ''),
    }
    
    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name', '').strip()
        quantity_needed = request.POST.get('quantity_needed', '').strip()
        urgency = request.POST.get('urgency', 'medium')
        reason = request.POST.get('reason', '').strip()
        
        # Validation
        if not medicine_name or not quantity_needed:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'requests/request_medicine.html', {'prefill_data': prefill_data})
        
        try:
            quantity_int = int(quantity_needed)
            if quantity_int <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            messages.error(request, "Please enter a valid quantity.")
            return render(request, 'requests/request_medicine.html', {'prefill_data': prefill_data})
        
        # Check if user is trying to request their own donation
        own_donation = Donation.objects.filter(
            donor=request.user,
            name__iexact=medicine_name
        ).exists()
        
        if own_donation:
            messages.error(request, f"You cannot request '{medicine_name}' because you donated it yourself. You can view it in your Track Donations page.")
            return render(request, 'requests/request_medicine.html', {'prefill_data': prefill_data})
        
        # Create the request
        medicine_request = MedicineRequest.objects.create(
            recipient=request.user,
            medicine_name=medicine_name,
            quantity=str(quantity_needed),
            urgency=urgency,
            reason=reason
        )
        
        messages.success(request, f"Your request for {medicine_name} has been submitted! Tracking code: {medicine_request.tracking_code}")
        return redirect('dashboard:recipient_dashboard')
    
    return render(request, 'requests/request_medicine.html', {'prefill_data': prefill_data})


@login_required
def track_medicine_requests(request):
    """View all medicine requests made by the user"""
    requests = MedicineRequest.objects.filter(recipient=request.user)
    return render(request, 'requests/track_medicine_requests.html', {'requests': requests})


@login_required
def medicine_request_detail(request, pk):
    """View details of a specific medicine request"""
    medicine_request = get_object_or_404(MedicineRequest, pk=pk, recipient=request.user)
    return render(request, 'requests/medicine_request_detail.html', {'request': medicine_request})


@login_required
def delete_medicine_request(request, pk):
    """Delete a medicine request (only by the requester)"""
    medicine_request = get_object_or_404(MedicineRequest, pk=pk, recipient=request.user)
    
    if request.method == 'POST':
        medicine_name = medicine_request.medicine_name
        medicine_request.delete()
        messages.success(request, f'Request for "{medicine_name}" has been deleted successfully.')
        return redirect('requests:track_medicine_requests')
    
    return render(request, 'requests/confirm_delete_request.html', {'medicine_request': medicine_request})
