from django import forms
from django.utils.safestring import mark_safe
from member.models import UserMember, Player


class UserMemberForm(forms.ModelForm):
    name = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs={'placeholder': 'John Smith'}))
    address_street = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs={'placeholder': '1 '
                                                                                                                 'Smith Street'}))
    address_town_city = forms.CharField(max_length=128, required=True,
                                        widget=forms.TextInput(attrs={'placeholder': 'Leeds '}))
    postcode = forms.CharField(max_length=12, required=True, widget=forms.TextInput(attrs={'placeholder': 'WF3 1UA'}))
    phone = forms.IntegerField(required=True)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    consent = forms.NullBooleanField(help_text=mark_safe("By consenting you are agreeing to the following: "
                                                         "<ul> "
                                                         "<li>I agree to my child receiving medication as "
                                                         "instructed on their record </li>"
                                                         "<li>I agree to emergency treatment by a qualified first "
                                                         "aider representing the club should the need arise </li>"
                                                         "<li>I agree to my child being photographed for the sole "
                                                         "usage in the promotion or celebration of activities of the "
                                                         "club </li>"
                                                         "<li>I agree to emergency treatment including the "
                                                         "administration of anaesthetics or blood transfusions as "
                                                         "considered necessary by the medial professionals present "
                                                         "should the need arise </li>"
                                                         "</ul>"))

    class Meta:
        model = UserMember
        fields = ('name', 'address_street', 'address_town_city', 'postcode', 'phone', 'consent')


class UserMemberAddChildForm(forms.ModelForm):
    #name = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs={'placeholder': 'John Smith'}))
    #birthdate = forms.DateField()
    #sex =  forms.CharField(max_length=1)
    #medical_details = forms.CharField(max_length=128, required=False)

    class Meta:
        model = Player
        exclude = ('member_parent',)
