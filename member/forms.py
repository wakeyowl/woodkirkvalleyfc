from django import forms
from django.http import request
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import UpdateView

from member.models import UserMember, Player, Accidents


class UserMemberForm(forms.ModelForm):
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
        fields = ('full_name', 'address1', 'address2', 'city', 'postcode', 'mobile_phone', 'consent')


class UserMemberAddChildForm(forms.ModelForm):
    birthdate = forms.DateField(input_formats=['%d/%m/%Y'], help_text='format=DD/MM/YYYY')

    class Meta:
        model = Player
        exclude = ('member_parent',)


class UserMemberUpdateForm(forms.ModelForm):
    class Meta:
        model = UserMember
        fields = ('address1', 'address2', 'city', 'postcode', 'mobile_phone',)


class AccidentForm(forms.ModelForm):
    class Meta:
        model = Accidents
        fields = ('accidenttype', 'person_injured', 'title', 'address', 'postcode', 'mobile_phone',
                  'accident_date', 'accident_injury', 'accident_location', 'accident_reason',
                  'first_aid_outcome', 'first_aid_given', 'first_aid_hospitalised', 'first_aid_person', 'hospital_more_than_24', 'hospital_name')
