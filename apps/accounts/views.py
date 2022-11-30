from django.views.generic import UpdateView, View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from accounts.models import Profile as ProfileModel
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class Profile(LoginRequiredMixin, UpdateView):
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