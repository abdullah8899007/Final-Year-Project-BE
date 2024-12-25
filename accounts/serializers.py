from django.conf import settings
from rest_framework import serializers
from custom_user.models import User
from .models import UserInfoModel
import re
#send mail 
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_staff', 'is_superuser']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input': 'password'}, write_only=True)
    phone = serializers.CharField(max_length=13, required=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "password2", "phone"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")  
        password2 = attrs.pop("password2", None)  # Remove 'password2' from the validated data

        if len(password) < 8:
            raise serializers.ValidationError("Password is too short")

        if password != password2:
            raise serializers.ValidationError("Passwords do not match")

        # phone = attrs.get("phone")
        # if not re.match(r'^\+\d{12}$', phone):
        #     raise serializers.ValidationError("Phone number format is invalid")

        return attrs


    def create(self, validated_data):
        phone = validated_data.pop("phone") 
        user = User.objects.create_user(**validated_data)
        UserInfoModel.objects.create(user=user, phone=phone)
        return user



class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)

    class Meta:
        model=User
        fields=["email","password"]



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_staff', 'is_superuser']


class ChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100, style={'input': 'password'}, write_only=True)
    password2=serializers.CharField(max_length=100, style={'input': 'password'}, write_only=True)

    class Meta:
        model=User
        fields=["password","password2"]

    def validate(self, attrs):
        password = attrs.get("password")  
        password2 = attrs.get("password2") 
        user=self.context.get("user")

        if len(password) < 8:
            raise serializers.ValidationError("Password is too short")
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordMailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email is not registered")

        # Create an instance of PasswordResetTokenGenerator
        token_generator = PasswordResetTokenGenerator()

        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = token_generator.make_token(user)
        link = 'http://localhost:8000/accounts/reset_password/'+uid+'/'+token

        subject = 'password reset mail Resturant app'
        message = f'Hi, {user.first_name} Pleasae click the link below to reset the password \n {link}'

        from_email = settings.EMAIL_HOST_USER  # Sender's email address

        send_mail(subject, message, from_email, [email], fail_silently=False)

        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100, style={'input': 'password'}, write_only=True)
    password2=serializers.CharField(max_length=100, style={'input': 'password'}, write_only=True)

    class Meta:
        model=User
        fields=["password","password2"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")  
            password2 = attrs.get("password2") 
            uid=self.context.get("uid")
            token=self.context.get("token")

            if len(password) < 8:
                raise serializers.ValidationError("Password is too short")
            if password != password2:
                raise serializers.ValidationError("Passwords do not match")
            id=smart_str(urlsafe_base64_decode(uid)) 

            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("token is not valid or expired")
            user.set_password(password)
            user.save()
            return attrs
        
        except DjangoUnicodeDecodeError :
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("token is not valid or expired")


