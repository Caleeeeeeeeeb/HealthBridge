from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import MedicineRequest
from donations.models import Donation


@login_required
@require_http_methods(["POST"])
def create_request(request):
    """Create a medicine request via AJAX"""
    try:
        medicine_name = request.POST.get('medicine_name', '').strip()
        quantity = request.POST.get('quantity', '').strip()
        urgency = request.POST.get('urgency', 'medium')
        reason = request.POST.get('reason', '').strip()
        donation_id = request.POST.get('donation_id', '').strip()
        
        # Debug logging
        print(f"=== CREATE REQUEST DEBUG ===")
        print(f"Medicine: {medicine_name}")
        print(f"Quantity: {quantity}")
        print(f"Urgency: {urgency}")
        print(f"Donation ID received: {donation_id}")
        
        # Validation
        if not medicine_name or not quantity:
            return JsonResponse({
                'success': False,
                'message': 'Please fill in all required fields'
            }, status=400)
        
        try:
            quantity_int = int(quantity)
            if quantity_int <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid quantity'
            }, status=400)
        
        # Get the donation if ID is provided
        matched_donation = None
        if donation_id:
            try:
                matched_donation = Donation.objects.get(id=donation_id, status=Donation.Status.AVAILABLE)
                print(f"Found donation: ID={matched_donation.id}, Name={matched_donation.name}, Donor={matched_donation.donor.username}, Current Qty: {matched_donation.quantity}")
                
                # Check if enough quantity is available
                if matched_donation.quantity < quantity_int:
                    return JsonResponse({
                        'success': False,
                        'message': f'Only {matched_donation.quantity} units available, but you requested {quantity_int}'
                    }, status=400)
                
                # Subtract the requested quantity from the donation
                matched_donation.quantity -= quantity_int
                print(f"Subtracting {quantity_int} from donation. New quantity: {matched_donation.quantity}")
                
                # If quantity reaches zero, mark as unavailable
                if matched_donation.quantity <= 0:
                    matched_donation.status = Donation.Status.DELIVERED
                    print(f"Donation quantity is now 0 - marking as DELIVERED")
                
                matched_donation.save()
                
            except Donation.DoesNotExist:
                print(f"Donation ID {donation_id} not found or not available")
        else:
            print("No donation_id provided")
        
        # Create the request
        medicine_request = MedicineRequest.objects.create(
            recipient=request.user,
            medicine_name=medicine_name,
            quantity=str(quantity),
            urgency=urgency,
            reason=reason,
            matched_donation=matched_donation,
            status=MedicineRequest.Status.MATCHED if matched_donation else MedicineRequest.Status.PENDING
        )
        
        print(f"Request created: ID={medicine_request.id}, Status={medicine_request.status}, Matched Donation={medicine_request.matched_donation_id}")
        
        return JsonResponse({
            'success': True,
            'message': 'Request submitted successfully',
            'tracking_code': medicine_request.tracking_code
        })
        
    except Exception as e:
        print(f"ERROR in create_request: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


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
            # Handle AJAX errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Please fill in all required fields'}, status=400)
            
            return render(request, 'requests/request_medicine.html', {'prefill_data': prefill_data})
        
        try:
            quantity_int = int(quantity_needed)
            if quantity_int <= 0:
                raise ValueError("Quantity must be positive")
        except ValueError:
            # Handle AJAX errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Please enter a valid quantity'}, status=400)
            
            return render(request, 'requests/request_medicine.html', {'prefill_data': prefill_data})
        
        # Check if user is trying to request their own donation
        own_donation = Donation.objects.filter(
            donor=request.user,
            name__iexact=medicine_name
        ).exists()
        
        if own_donation:
            # Handle AJAX errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'You cannot request your own donation'}, status=400)
            
            return render(request, 'requests/request_medicine.html', {'prefill_data': prefill_data})
        
        # Create the request
        medicine_request = MedicineRequest.objects.create(
            recipient=request.user,
            medicine_name=medicine_name,
            quantity=str(quantity_needed),
            urgency=urgency,
            reason=reason
        )
        
        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Request submitted successfully', 'tracking_code': medicine_request.tracking_code})
        
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
@login_required
def delete_medicine_request(request, pk):
    """Delete a medicine request (only by the requester)"""
    if request.method == 'POST':
        try:
            medicine_request = get_object_or_404(MedicineRequest, pk=pk, recipient=request.user)
            medicine_name = medicine_request.medicine_name
            medicine_request.delete()
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'success': True, 'message': f'Request for "{medicine_name}" has been deleted successfully.'})
            
            return redirect('requests:track_medicine_requests')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'success': False, 'error': str(e)})
            return redirect('requests:track_medicine_requests')
    
    # For GET requests, show confirmation page
    medicine_request = get_object_or_404(MedicineRequest, pk=pk, recipient=request.user)
    return render(request, 'requests/confirm_delete_request.html', {'medicine_request': medicine_request})


@login_required
@require_http_methods(["POST"])
def deliver_medicine(request, pk):
    """Mark a medicine request as fulfilled (donor delivers the medicine)"""
    try:
        # Get the request and verify the donor owns the matched donation
        medicine_request = get_object_or_404(MedicineRequest, pk=pk)
        
        # Verify the donor owns the matched donation
        if not medicine_request.matched_donation or medicine_request.matched_donation.donor != request.user:
            return JsonResponse({
                'success': False,
                'message': 'You do not have permission to deliver this medicine'
            }, status=403)
        
        # Update statuses
        medicine_request.status = MedicineRequest.Status.FULFILLED
        medicine_request.save()
        
        # Don't change donation status - it was already handled during request creation
        # The donation quantity was already subtracted and status only changes to DELIVERED when quantity = 0
        
        return JsonResponse({
            'success': True,
            'message': 'Medicine marked as delivered successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
@require_http_methods(["POST"])
def claim_medicine(request, pk):
    """Mark a medicine request as claimed (recipient claims the medicine)"""
    try:
        # Get the request and verify the user is the recipient
        medicine_request = get_object_or_404(MedicineRequest, pk=pk, recipient=request.user)
        
        # Can only claim if status is fulfilled
        if medicine_request.status != MedicineRequest.Status.FULFILLED:
            return JsonResponse({
                'success': False,
                'message': 'This medicine is not ready to be claimed yet'
            }, status=400)
        
        # Update status to claimed
        medicine_request.status = MedicineRequest.Status.CLAIMED
        medicine_request.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Medicine claimed successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
