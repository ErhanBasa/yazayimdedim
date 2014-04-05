# -*- coding: utf-8 -*-

from django import forms
from blog.models import Contact
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('date',)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {"placeholder": u"İsim Soyisim"}
        self.fields['mail'].widget.attrs = {"placeholder": u"E-Posta Adresiniz"}
        self.fields['subject'].widget.attrs = {"placeholder": u"Konu Neydi?"}
        self.fields['message'].widget.attrs = {"placeholder": u"Mesajınız.."}


class RegisterationForm(UserCreationForm):
    email = forms.EmailField(u"E-Posta Adresi")

    def __init__(self, *args, **kwargs):
        super(RegisterationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {"placeholder": u"KULLANICI ADI"}
        self.fields['password1'].widget.attrs = {"placeholder": u"ŞİFRE"}
        self.fields['password2'].widget.attrs = {"placeholder": u"ŞİFRE (TEKRAR)"}
        self.fields['email'].widget.attrs = {"placeholder": u"E-POSTA ADRESİNİZ"}
    pass

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs = {"placeholder": u"KULLANICI ADI"}
        self.fields['password'].widget.attrs = {"placeholder": u"ŞİFRE"}