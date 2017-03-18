from django import forms
from django.views.generic.edit import UpdateView
from django.utils.safestring import mark_safe
from member.models import UserMember, Player


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
    birthdate = forms.DateField(help_text='DD/MM/YYYY', widget=forms.DateInput(format='%d/%m/%Y'),
                                 input_formats=('%d/%m/%Y',))
    class Meta:
        model = Player
        exclude = ('member_parent',)
