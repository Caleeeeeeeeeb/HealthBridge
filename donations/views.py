from datetime import datetime, date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from healthbridge_app.models import GenericMedicine
from .models import Donation


@login_required
def donate_medicine(request):
    """Create a new medicine donation"""
    if request.method == "POST":
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        expiry_date_str = request.POST.get("expiry_date")
        image = request.FILES.get("image")

        if name and quantity and expiry_date_str:
            # Validate expiry date is not in the past
            try:
                expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                today = date.today()
                
                if expiry_date < today:
                    messages.error(request, f"Cannot donate expired medicine. The expiry date ({expiry_date_str}) has already passed.")
                    return render(request, "donations/donate_medicine.html")
                
                Donation.objects.create(
                    name=name,
                    quantity=quantity,
                    expiry_date=expiry_date,
                    donor=request.user,
                    image=image,
                )
                messages.success(request, f"Thank you for donating {quantity}x {name}! You can track it under Track Requests.")
                # Redirect to appropriate dashboard based on user role
                if request.user.is_donor:
                    return redirect("dashboard:donor_dashboard")
                elif request.user.is_recipient:
                    return redirect("dashboard:recipient_dashboard")
                return redirect("select_role")
            except ValueError:
                messages.error(request, "Invalid date format. Please use a valid date.")
                return render(request, "donations/donate_medicine.html")
        
        messages.error(request, "Please fill in all fields.")
    return render(request, "donations/donate_medicine.html")


@login_required
def my_donations(request):
    """View all donations made by the current user"""
    items = Donation.objects.filter(donor=request.user).order_by("-donated_at")
    return render(request, "donations/track_requests_list.html", {"items": items})


@login_required
def donation_detail(request, pk: int):
    """View details of a specific donation"""
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)
    return render(request, "donations/track_request_detail.html", {"donation": donation})


@login_required
def delete_donation(request, pk):
    """Delete a donation (only by the donor)"""
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)
    
    if request.method == 'POST':
        medicine_name = donation.name
        donation.delete()
        messages.success(request, f'Donation "{medicine_name}" has been deleted successfully.')
        return redirect('donations:my_donations')
    
    return render(request, 'donations/confirm_delete_donation.html', {'donation': donation})


def medicine_search(request):
    """Search for available medicines with expiry date range filter"""
    query = request.GET.get('q', '').strip()
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()
    
    medicines = Donation.objects.all()
    filter_message = None
    filter_error = None

    # Apply name search
    if query:
        medicines = medicines.filter(name__icontains=query)

    # Apply expiry date range filter
    if start_date or end_date:
        try:
            if start_date and end_date:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                
                if start > end:
                    filter_error = "Start date cannot be after end date."
                else:
                    medicines = medicines.filter(expiry_date__range=[start, end])
                    filter_message = f"Showing medicines expiring between {start_date} and {end_date}"
            
            elif start_date:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                medicines = medicines.filter(expiry_date__gte=start)
                filter_message = f"Showing medicines expiring from {start_date} onwards"
            
            elif end_date:
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                medicines = medicines.filter(expiry_date__lte=end)
                filter_message = f"Showing medicines expiring up to {end_date}"
                
        except ValueError:
            filter_error = "Invalid date format. Please use YYYY-MM-DD."

    return render(request, 'donations/medicine_search.html', {
        'medicines': medicines,
        'query': query,
        'start_date': start_date,
        'end_date': end_date,
        'filter_message': filter_message,
        'filter_error': filter_error,
    })


def medicine_autocomplete(request):
    """API endpoint for medicine name autocomplete suggestions with caching"""
    query = request.GET.get('q', '').strip().lower()
    
    # Return empty if query too short
    if not query or len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    # Try to get from cache first (cache for 5 minutes)
    cache_key = f'autocomplete_{query}'
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return JsonResponse({'suggestions': cached_result})
    
    # Get unique medicine names from donations
    donation_medicines = Donation.objects.filter(
        name__icontains=query
    ).values_list('name', flat=True).distinct()[:5]
    
    # Get unique medicine names from generic medicines  
    generic_medicines = GenericMedicine.objects.filter(
        name__icontains=query
    ).values_list('name', flat=True).distinct()[:5]
    
    # Combine and deduplicate
    all_medicines = list(set(list(donation_medicines) + list(generic_medicines)))
    suggestions = sorted(all_medicines)[:10]  # Limit to 10 suggestions
    
    # Cache the result for 5 minutes (300 seconds)
    cache.set(cache_key, suggestions, 300)
    
    return JsonResponse({'suggestions': suggestions})
