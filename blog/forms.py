# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from blog.models import Contact, Profile
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
    check_agreement = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {"placeholder": u"KULLANICI ADI"}
        self.fields['password1'].widget.attrs = {"placeholder": u"ŞİFRE"}
        self.fields['password2'].widget.attrs = {"placeholder": u"ŞİFRE (TEKRAR)"}
        self.fields['email'].widget.attrs = {"placeholder": u"E-POSTA ADRESİNİZ"}
    
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username__iexact=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_check_agreement(self):
        check_agreement = self.cleaned_data["check_agreement"]
        if check_agreement == False:
            raise forms.ValidationError(
                u"Lütfen üyelik sözleşmesini kabul ediniz."
            )
        return check_agreement

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {"placeholder": u"KULLANICI ADI"}
        self.fields['password'].widget.attrs = {"placeholder": u"ŞİFRE"}

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['about'].widget.attrs = {"placeholder": u"Hakkınızda 200 karakterlik bir yazı giriniz..", "maxlength": "200"}
        self.fields['facebook_url'].widget.attrs = {"placeholder": u"Facebook Kullanıcı Adınız"}
        self.fields['twitter_url'].widget.attrs = {"placeholder": u"Twitter Kullanıcı Adınız"}

    class Meta:
        model = Profile
        exclude = ('user',)
