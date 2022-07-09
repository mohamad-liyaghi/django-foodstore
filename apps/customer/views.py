from django.views.generic import TemplateView, ListView
from django.db.models import Q

from restaurant.models import Food, Category


class HomePageView(TemplateView):
    '''
        Home page
    '''
    template_name = "customer/home.html"

class CartPageView(TemplateView):
    '''
        Show user orders
    '''
    template_name = "customer/cart.html"


class FoodSearchView(ListView):
    '''
        Show result of searched data
    '''
    template_name = "customer/food-list.html"
    context_object_name = "foods"

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        return Food.objects.filter(
            Q(name__icontains=q) | Q(category__title= q)
        ).order_by("-is_available")
