from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings

class ContactForm(forms.Form):
    name = forms.CharField(label='名前') # 名前
    message = forms.CharField(label='お問い合わせ内容', widget=forms.Textarea) #問い合わせ内容

    # メール送信処理
    def send_email(self):
        # send email using the self.cleaned_data dictionary
        subject = self.cleaned_data['name']
        message = self.cleaned_data['message']
        from_email = settings.EMAIL_HOST_USER
        to = [settings.EMAIL_HOST_USER]

        send_mail(subject, message, from_email, to)
