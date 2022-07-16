from django.views.generic import TemplateView, ListView, View, DetailView
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import  messages
from django.template import RequestContext

import  random


from restaurant.models import Food, Category
from customer.models import Order

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

class CartAddView(View):
    # add an item to cart
    def get(self, request, food_id):
        cart = Cart(request)
        food = get_object_or_404(Food, id= food_id)

        if food.is_available:
            cart.add(food, 1)
            messages.success(self.request, "Food added to your cart")
        return redirect('customer:cart-page')

class CartRemoveView(View):
    # remove an item form cart
    def get(self, request, food_id):
        cart = Cart(request)
        food = get_object_or_404(Food, id=food_id)
        cart.remove(food)
        messages.success(self.request, "Item removed from your cart")
        return redirect('customer:cart-page')

class OrderCreateView(LoginRequiredMixin, View):
    # create a new order
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user= request.user, orderid= random.randint(10000000000000,99999999999999),
                                     total_price= cart.get_total_price())
        for food in cart:
            object = get_object_or_404(Food, name= food["product"])

            if object.is_available:
                order.items.add(food["product"])
                object.inventory -= 1
                object.save()
        cart.clear()
        order.save()
        messages.success(self.request, "Order created successfully")
        return  redirect("customer:cart")

class OrderDetailView(LoginRequiredMixin, DetailView):
    # show detail of an order
    template_name = "customer/order-detail.html"

    def get_object(self):
        return get_object_or_404(Order, id= self.kwargs["id"], orderid= self.kwargs["orderid"])


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