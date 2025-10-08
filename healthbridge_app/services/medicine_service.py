from ..models import GenericMedicine, BrandMedicine
from django.db.models import Q

class MedicineService:
    @staticmethod
    def search_medicines(user_input):
        """
        Retrieves all medicines (generic + branded) related to user input.
        """
        user_input = user_input.strip().lower()

        # Find generic matches
        generics = GenericMedicine.objects.filter(name__icontains=user_input)

        # Find brand matches linked to any matching generics or direct brand name
        brands = BrandMedicine.objects.filter(
            Q(generic__in=generics) | Q(brand_name__icontains=user_input)
        ).select_related('generic')

        result = {
            "input": user_input,
            "generic_matches": list(generics.values_list('name', flat=True)),
            "brand_matches": [
                {
                    "brand_name": b.brand_name,
                    "generic_name": b.generic.name
                } for b in brands
            ]
        }
        return result
