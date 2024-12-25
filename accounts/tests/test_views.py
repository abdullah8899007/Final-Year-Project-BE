from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
User = get_user_model()

class UserListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()       
        self.user = User.objects.create_user(email='user@gmail.com', password="]'/[;.pl]")
    #     self.super_user = User.objects.create_superuser(email='superuser@gmail.com', password="]'/[;.pl]")

    # def test_staff_user(self):
    #     self.client.login(email='superuser@gmail.com', password="]'/[;.pl]")
    #     response = self.client.get(reverse("all_users"))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_staff_user(self):
        self.client.login(email='user@gmail.com', password="]'/[;.pl]")
        response = self.client.get(reverse("all_users"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_registration(self):
        data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "testpassword",
            "password2": "testpassword",
            "phone": "+920000000000"
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_data(self):
        data = {
            "email": "testexample.com", # invalid field 
            "first_name": "John",
            "last_name": "Doe",
            "password": "testpassword",
            "password2": "testpassword",
            "phone": "kjkjbjbjhhjb",    # invalid fi eld
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

    def test_field_required(self):
        data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "testpassword",
            "password2": "testpassword",
            # "phone": "+920000000000"     #missing field
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 




class UserLoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')

    def test_login(self):
        test_user = User.objects.create_user(email="abc@gmail.com", password="]'/[;.pl]")

        data = {
            "email": "abc@gmail.com",
            "password": "]'/[;.pl]",
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_not_exists(self):
        test_user = User.objects.create_user(email="abc@gmail.com", password="]'/[;.pl]")

        data = {
            "email": "xyz@gmail.com",
            "password": "]'/[;.pl]",
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_field_required(self):
        test_user = User.objects.create_user(email="abc@gmail.com", password="]'/[;.pl]")

        data = {
            "email": "xyz@gmail.com",
            # "password": "]'/[;.pl]",   # missing fields 
        }

        response = self.client.post(self.login_url, data, format='json')



class ViewUserTest(APITestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(email="abc@gmail.com", password="]'/[;.pl]")
        self.client.force_authenticate(user=self.test_user)

    def test_view_user(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)




class AuthenticatedAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(email='user@gmail.com', password="]'/[;.pl]")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

class ChangePasswordTest(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.change_url = reverse('set_password')

    def test_change_password(self):
        data = {
            "password": "newpassword",
            "password2": "newpassword",
        }

        response = self.client.post(self.change_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_not_match(self):
        data = {
            "password": "newpassword",
            "password2": "new0password",
        }

        response = self.client.post(self.change_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_field_required(self):
        data = {
            "password": "newpassword",
            # "password2": "newpassword", # missing field
        }

        response = self.client.post(self.change_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




class ChangePasswordTest(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.change_url = reverse('send_password_mail')

    def test_send_mail(self):
        data = {
            "email":'user@gmail.com'
        }

        response = self.client.post(self.change_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_not_exists(self):
        data = {
            "email":'abc@gmail.com'
        }

        response = self.client.post(self.change_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




class UpdateUserTest(AuthenticatedAPITestCase):
    def setUp(self):
        super().setUp()
        self.update_url = reverse('update_user')

    def test_registration(self):
        data = {
            "first_name": "hello",
            "last_name": "world",
        }

        response = self.client.patch(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
