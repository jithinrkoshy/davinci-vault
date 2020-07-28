from django import forms
from davinci.models import USER_DATA


class USER_DATA_FORM(forms.ModelForm):
    email = forms.EmailField(required=True)
    country_code = forms.ChoiceField(choices = [('91','91'),('92','92'),('93','93')],required=False)
    mobile_number = forms.IntegerField(required = False)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)
    class Meta():
        model = USER_DATA
        fields = ('email','first_name','last_name','country_code','mobile_number')

        widgets = {

          'email' : forms.EmailInput(attrs = {'id':'email-input','placeholder':'Enter your email'}),
          'first_name' : forms.TextInput(attrs = {'id':'first-name','placeholder':'Enter firstname'}),
          'last_name' : forms.TextInput(attrs = {'id':'last-name','placeholder':'Enter lastname'}),
          'country_code' : forms.Select(attrs = {'id':'country-code'}),
          'mobile_number' : forms.NumberInput(attrs = {'id':'mobile-number'}),



        }
