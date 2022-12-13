from django.views.generic import TemplateView, ListView, View, DetailView
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import  messages

import  random

from restaurant.models import Food, Category
from customer.models import Order, OrderItem

from .cart import Cart

class HomePageView(TemplateView):
    '''
        Home page
    '''
    template_name = "customer/home.html"
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by("food_category")[:5]
        return context


class CartPageView(View):
    '''
        Show user orders
    '''

    def get(self, request):
        cart = Cart(request)
        orders = Order.objects.filter(user= request.user)
        return render(request, "customer/cart.html", {'cart': cart, "orders" : orders})


class CartAddView(LoginRequiredMixin, View):
    '''Add sth to cart (sessions)'''

    def get(self, request, token):
        cart = Cart(request)
        food = get_object_or_404(Food, token=token)

        if request.user == food.provider.owner:
            messages.success(self.request, "You can not order your restaurants food.", "warning")
            return redirect('restaurant:food-detail', token=food.token)

        if food.is_available:
            cart.add(food, 1)
            messages.success(self.request, "Food added to your cart", "success")
            return redirect('restaurant:food-detail', token=food.token)

        messages.success(self.request, "Sorry, this item is unavailable", "danger")
        return redirect('restaurant:food-detail', token=food.token)


class CartRemoveView(View):
    """Remove an item from cart"""

    def get(self, request, token):
        cart = Cart(request)
        food = get_object_or_404(Food, token=token)
        cart.remove(food)
        messages.success(self.request, "Item removed from your cart")
        return redirect('customer:cart-page')



class OrderCreateView(LoginRequiredMixin, View):
    '''Create a new order'''

    def get(self, request):
        cart = Cart(request)

        if cart:
            order = Order.objects.create(user=request.user)
            for item in cart:
                try:
                    OrderItem.objects.create(order=order, item=item['product'], quantity=item['quantity'])
                except:
                    pass

            cart.clear()
            messages.success(self.request, "Order created successfully", "success")
            return redirect("customer:cart-page")

        messages.success(self.request, "Cart is empty.", "warning")
        return redirect("customer:cart-page")


class OrderDetailView(LoginRequiredMixin, DetailView):
    # show detail of an order
    template_name = "customer/order-detail.html"

    def get_object(self):
        return get_object_or_404(Order, order_id=self.kwargs["order_id"])
    
    def get_context_data(self, **kwargs):        
        data = super().get_context_data(**kwargs)
        data["items"] = self.get_object().items.all()
        return data


class OrderPayView(LoginRequiredMixin, View):
    # page in order to pay for order
    # you have to add your custom payment method
    def get(self, request, id, orderid):
        order = get_object_or_404(Order, id=id, orderid= orderid)
        order.is_paid = True
        order.status = "preparing"
        order.save()
        return redirect("customer:cart-page")

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



def handler404 (request, exception):
    return render(request, "errors/404.html", {})

def handler500 (request, exception=None):
    return render(request, "errors/500.html", {})