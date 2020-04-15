from django import forms

class BankForm(forms.Form):
    PurchaseAmt = forms.DecimalField(decimal_places=2, widget=forms.TextInput(attrs={'readonly':'readonly','type':'hidden'}))
    PurchaseDesc = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    CountryCode = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'readonly','type':'hidden'}))
    CurrencyCode = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'readonly','type':'hidden'}))
    MerchantName = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'readonly':'readonly','type':'hidden'}))
    MerchantURL = forms.URLField(widget=forms.TextInput(attrs={'readonly':'readonly','type':'hidden'}))
    MerchantCity = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','type':'hidden'}))
    MerchantID = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','type':'hidden'}))
    #SuccessURL = forms.URLField(widget=forms.TextInput(attrs={'readonly':'readonly','type':'hidden'}))
    #FailURL = forms.URLField(widget=forms.TextInput(attrs={'readonly':'readonly','type':'hidden'}))
    CardholderName= forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','type':'hidden'}))
   # value = "Y" / >
    Email=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','type':'hidden'}))
    #value = "Y" / >
    Phone=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly','type':'hidden'}))











