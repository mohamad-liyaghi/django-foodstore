from django.views.generic import UpdateView, View, FormView, ListView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import  messages

from accounts.models import Profile as ProfileModel, Request
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RequestForm


class ProfileView(LoginRequiredMixin, UpdateView):
    '''
        Profile page. 
        Only the profile owner can update this page.
    '''

    template_name = "account/profile.html"
    context_object_name = "profile"

    fields = ["first_name", "last_name", "country", "city", 
                "detailed_address", "phone_number", "passport_number"]

    def get_object(self):
        # return users profile if there wasnt an id
        try:
             userid = self.kwargs["id"]

        except:
             return get_object_or_404(ProfileModel, 
                        user=self.request.user)
        
        return get_object_or_404(ProfileModel, 
                user__userid=userid)
    
    def get_success_url(self) -> str:
        return reverse_lazy("accounts:profile", 
                    kwargs={"id" : self.kwargs.get("id")})


class MoneyView(LoginRequiredMixin, View):
    '''You should implement payment method in here.'''
    
    def get(self, request):
        request.user.balance = request.user.balance + 20
        request.user.save()
        return HttpResponse("20 coins added to your balance.")


class RequestCreateView(LoginRequiredMixin, FormView):
    '''Request to become admin'''

    def dispatch(self, request, *args, **kwargs):
        '''Admin users can blocked users can not add request.'''

        # admin users can not request to become an admin
        if self.request.user.is_admin:
            messages.success(self.request, "You are already an admin.")
            return redirect("customer:home")
        
        # check if user is blocked or even there is a blocked request
        elif self.request.user.is_blocked or self.request.user.requests.filter(status="b"):
            messages.success(self.request, "Blocked users can not request.")
            return redirect("customer:home")
        
        # check if user has a pending request
        elif self.request.user.requests.filter(status="p"):
            messages.success(self.request, "You have already a pending request.")
            return redirect("customer:home")
        
        return super().dispatch(request, *args, **kwargs)
    

    template_name = "request/request-add.html"
    form_class = RequestForm
    success_url = reverse_lazy("customer:home")


    def get_form_kwargs(self):
        kwargs = super(RequestCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Request sent, wait for results.")
        return super(RequestCreateView, self).form_valid(form)
        
        
class RequestListView(LoginRequiredMixin, ListView):
    '''
        List of requests.
        Admins see all requests.
        Normal Users just see their own requests
    '''

    template_name = "request/request-list.html"
    context_object_name = "requests"

    def get_queryset(self):
        if self.request.user.is_admin:
            return Request.objects.filter(status="p")

        return Request.objects.filter(user=self.request.user)


class RequestDetailView(LoginRequiredMixin, UpdateView):
    '''
        Request detail page.
        Admins and request owner can access this page.
        Admins can accept/decline/block this request 
        Request owner can see or update(When its pending).
    '''
    
    def dispatch(self, request, *args, **kwargs):
        '''Admin users and request owner can access this page.'''

        if self.request.user.is_admin or self.get_object().user == self.request.user:
            return super().dispatch(request, *args, **kwargs)

        messages.success(self.request, "You can not access this page.")
        return redirect("customer:home")

    template_name = "request/request-update.html"
    fields = []
    
    def get_object(self):
        return get_object_or_404(Request, token=self.kwargs["token"])

