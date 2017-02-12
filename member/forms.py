from django import forms
from django.contrib.auth.models import User

from member.models import Member


class MemberForm(forms.ModelForm):
    name = forms.CharField(max_length=128, required=True, help_text="Please enter your full name.")
    address = forms.CharField(max_length=128, required=False)
    postcode = forms.CharField(max_length=12, required=False)
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=True)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    consent = forms.BooleanField()

    class Meta:
        model = Member
        fields = ('name', 'address', 'postcode', 'email', 'phone', 'consent' )
