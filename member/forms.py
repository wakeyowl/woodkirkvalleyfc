from django import forms
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget
from django.http import request
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import UpdateView
from django.contrib.admin.widgets import AdminDateWidget

from member.models import UserMember, Player, Accident


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
        fields = (
            'full_name', 'address1', 'address2', 'city', 'postcode', 'mobile_phone', 'consent',
            'accepted_code_of_conduct',)


class UserMemberAddChildForm(forms.ModelForm):
    birthdate = forms.DateField(input_formats=['%d/%m/%Y'], help_text='format=DD/MM/YYYY')
    picture = forms.ImageField(required=False, help_text=mark_safe(
        "Please ensure the picture is square (1:1) and orientation is correct on the profile page after updating."))
    class Meta:
        model = Player
        exclude = ('member_parent',)


class UserMemberUpdateForm(forms.ModelForm):
    class Meta:
        model = UserMember
        fields = ('address1', 'address2', 'city', 'postcode', 'mobile_phone', 'accepted_code_of_conduct',)


class UserMemberUpdatePlayerForm(forms.ModelForm):
    picture = forms.ImageField(required=False, help_text=mark_safe(
        "Please ensure the picture is square (1:1) and orientation is correct on the profile page after updating."))
    is_active = forms.NullBooleanField(help_text=mark_safe("I want to enroll for the current season."))
    accepted_code_of_conduct = forms.NullBooleanField(
        help_text=mark_safe("I have read and accept the Player Club Code of Conduct"))

    class Meta:
        model = Player
        fields = ('name', 'gender', 'birthdate', 'accepted_code_of_conduct', 'manager', 'picture', 'is_active',)


class AccidentForm(forms.ModelForm):
    accident_date = forms.DateField(widget=SelectDateWidget(empty_label="Nothing"), )

    class Meta:
        model = Accident
        fields = ('accident_type', 'person_injured', 'person_injured_address', 'person_injured_postcode',
                  'person_injured_mobile_phone',
                  'accident_date', 'injury_sustained', 'accident_location', 'accident_reason',
                  'first_aid_outcome', 'first_aid_person', 'first_aid_given', 'first_aid_hospitalised',
                  'hospital_more_than_24', 'hospital_name')
