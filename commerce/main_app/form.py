from django import forms
from .models import *
from django.core.exceptions import ValidationError


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['name','color', 'description','cat','dual','memory','os',
         'battery','hearing','camera','dimensions','display','status','price','currency','brand']
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(PhoneForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['name'].required = True
        self.fields['description'].required = True
        self.fields['cat'].required = True
        self.fields['color'].required = True
        self.fields['cat'].required = True
        self.fields['dual'].required = True
        self.fields['memory'].required = True
        self.fields['os'].required = True
        self.fields['battery'].required = True
        self.fields['hearing'].required = True
        self.fields['camera'].required = True
        self.fields['dimensions'].required = False
        self.fields['display'].required = True
        self.fields['price'].required = True
        self.fields['currency'].required = True
        self.fields['brand'].required = True

   
 

class BillingForm(forms.ModelForm):
    address_02 = forms.CharField(required=False)
    country = forms.CharField(required=False)
    postcode = forms.CharField(required=False)
    address_02 = forms.CharField(required=False)
    town_city = forms.CharField(required=False)
    district = forms.CharField(required=False)

    class Meta:
        model = Billing
        fields = ['firstname','lastname','company','phone','email','country','address_01',
        'address_02','town_city','district','postcode']


class ChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = ['product','quantity','total']


       