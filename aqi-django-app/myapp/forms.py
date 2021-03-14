from django import forms
from .models import *
from django.contrib.auth import get_user_model

class customSignupForm(forms.ModelForm):
    ACCOUNT_TYPES = ((1,'Investor'),(2,'Developer'))
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPES)
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'account_type']
    def save(self, user):
    	user.save() 
    	account_type_filled = self.cleaned_data['account_type']
    	print int(account_type_filled)
    	print type(account_type_filled)
    	if int(account_type_filled)==1:
    		print "Creating investor account"
    		investor=Investor()
    		investor.useraccount=user
    		investor.save()
    	elif int(account_type_filled)==2:
    		print "Creating developer account"
    		developer = Developer()
    		developer.useraccount=user
    		developer.save()
                       
