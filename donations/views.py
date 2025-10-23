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
        expiry_date = request.POST.get("expiry_date")
        image = request.FILES.get("image")

        if name and quantity and expiry_date:
            Donation.objects.create(
                name=name,
                quantity=quantity,
                expiry_date=expiry_date,
                donor=request.user,
                image=image,
            )
            messages.success(request, f"Thank you for donating {quantity}x {name}! You can track it under Track Requests.")
            return redirect("dashboard")
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
        return redirect('dashboard')
    
    return render(request, 'donations/confirm_delete_donation.html', {'donation': donation})


def medicine_search(request):
    """Search for available medicines"""
    query = request.GET.get('q', '').strip()
    medicines = Donation.objects.all()

    if query:
        medicines = medicines.filter(name__icontains=query)

    return render(request, 'donations/medicine_search.html', {
        'medicines': medicines,
        'query': query
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
