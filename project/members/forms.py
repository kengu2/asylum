# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.functional import allow_lazy, lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from phonenumber_field.formfields import PhoneNumberField

from .models import MembershipApplication


def rules_accepted_proxy(msg):
    return msg % settings.APPLICATION_RULES_URL


rules_accepted_proxy = allow_lazy(rules_accepted_proxy, str)


class ApplicationForm(forms.ModelForm):
    rules_accepted = forms.BooleanField(required=True, label=rules_accepted_proxy(_("I have read and accept <a href=\"%s\" target=\"_blank\">the rules</a>")))
    monthlymember = forms.BooleanField(required=False, label=_("I want 24/7 access to hacklab and tools with monthly fee"),initial=True)
    phone = PhoneNumberField(required=False,widget=forms.TextInput(attrs={'placeholder': '+358403456789'}),help_text=_("Phonenumber will also be your access key if you choose 24/7 access, international format"))
    monthlyPayment = forms.CharField(label=_("Monthly fee"),initial='20',widget=forms.TextInput(attrs={'placeholder': '20'}),help_text=_("I want to pay this much per month"))
    paymentInterval = forms.CharField(label=_("Payment interval"),initial='3',widget=forms.TextInput(attrs={'placeholder': '3'}),help_text=_("I want to have invoice every X months<br>ex. 20€/month every 3 months will give you an invoice of 60€ every 3 months"))

    required_css_class = 'required'

    class Meta:
        model = MembershipApplication
        fields = [
            'fname',
            'lname',
            'city',
            'email',
            'phone',
            'nick',
            'monthlymember',
            'monthlyPayment',
            'paymentInterval'
        ]
