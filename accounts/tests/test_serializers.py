from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from accounts.serializers import (UserRegistrationSerializer, SendPasswordMailSerializer,
ChangePasswordSerializer,UserLoginSerializer)


User = get_user_model()


class UserRegiatrationSerializerTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration_serializer(self):
        data = {
            "email": "example@yahoo.com",
            "first_name": "hello",
            "last_name": "world",
            "password": "]'/[;.pl]",
            "password2": "]'/[;.pl]",
            "phone": "+920000000000"
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_field_required(self):
        data = {
            "email": "example@yahoo.com",
            "first_name": "hello",
            "last_name": "world",
            "password": "]'/[;.pl]",
            # "password2": "]'/[;.pl]",
            "phone": "+920000000000"
        }
        serializer = UserRegistrationSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
            
    def test_invalid_field(self):
        data = {
            "email": "exampleyahoo.com",  # invalid data 
            "first_name": "hello",
            "last_name": "world",
            "password": "]'/[;.pl]",
            "password2": "]'/[;.pl]",
            "phone": "+920000000000"
        }
        serializer = UserRegistrationSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)




class MailSerializerTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_send_password_mail_serializer(self):
        test_user = User.objects.create_user(email="abc@gmail.com", password="]'/[;.pl]")

        data = {
            "email": "abc@gmail.com"
        }
        serializer = SendPasswordMailSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_email_notfound(self):
        test_user = User.objects.create_user(email="abc@gmail.com", password="]'/[;.pl]")

        data = {
            "email": "bbb@gmail.com"
        }
        serializer = SendPasswordMailSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)




class ChangePasswordSerializerTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create_user(email="abc@gmail.com", password="]'/[;.pl]")

    def test_change_password_serializer(self):
        data = {
            'password': 'newpassword',
            'password2': 'newpassword'
        }
        serializer = ChangePasswordSerializer(data=data, context={'user': self.test_user})
        self.assertTrue(serializer.is_valid())

    def test_password_too_short(self):
        data = {
            'password': 'short',
            'password2': 'short'
        }
        serializer = ChangePasswordSerializer(data=data, context={'user': self.test_user})

        # Ensure that a ValidationError is raised with the appropriate message
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

    def test_password_not_matching(self):
        data = {
            'password': 'passwordone',
            'password2': 'password2'
        }
        serializer = ChangePasswordSerializer(data=data, context={'user': self.test_user})
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)




class LoginSerializerTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create_user(email="abc@gmail.com", password="]'/[;.pl]")

    def test_login(self):

        data = {
            "email": "abc@gmail.com",
            "password":"]'/[;.pl]"
        }
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())


        

