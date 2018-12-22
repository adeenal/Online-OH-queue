from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from .verify_tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):

    def validate_email(self, email):
        if "upenn.edu" not in email:
            raise serializers.ValidationError("Email is not a Penn Email")
        return email

    class Meta:
        model = models.StudentUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('email', 'first_name', 'last_name', 'password', )

    def create(self, validated_data):
        user =  models.StudentUser.objects.create(**validated_data)
        user.is_active = False
        user.username = user.email.split("@")[0]
        user.set_password(user.password)
        user.save()

        # email verification
        current_site = settings.SITE_URL
        mail_subject = 'Activate your office hours account'
        message = "Hi {username}, \n Please click on the link to confirm your registration, \nhttp://{domain}/activate/{uid}/{token} \n".format(username=user.username, domain=current_site, uid=urlsafe_base64_encode(force_bytes(user.pk)).decode(), token=account_activation_token.make_token(user))
        to_email = user.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()

        return user