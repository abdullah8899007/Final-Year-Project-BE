from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from custom_user.models import User
from .serializers import *
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from rest_framework import filters
from .permissions import IsStaff


#create views here 
class UserList(APIView):
    permission_classes = [IsStaff]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email']

    def get(self, request):
        query = request.query_params.get('search')
        users = User.objects.all()
        if query:
            users = users.filter(email__icontains=query)
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistration(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key, "message": "User registered successfully."}, status=status.HTTP_201_CREATED)


class UserLogin(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key, "message": "Login successful."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Email or password is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewUser(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)  
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordEmail(APIView):
    def post(self, request, format=None):
        serializer = SendPasswordMailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"message": "Password reset link has been sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(APIView):
    def post(self, request, uid, token, format=None):
        serializer = ForgotPasswordSerializer(data=request.data, context={"uid":uid, "token":token})
        if serializer.is_valid(raise_exception=True):
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.session.flush()
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
    

class UpdateUser(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, format=None):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User profile updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#google login
class GoogleLogin(APIView):
    def get(self, request):
        # Construct the authorization URL
        google_auth_url = "https://accounts.google.com/o/oauth2/auth"
        client_id = '573527958199-2d0jv8ejnfpanrd21odm85iu3u2sa8cc.apps.googleusercontent.com'
        redirect_uri = 'http://localhost:8000/accounts/google/login/callback/'
        scope = 'openid email profile'
        state = 'random_state_value'

        authorization_url = f"{google_auth_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}&response_type=code"

        # Redirect the user to the authorization URL
        return HttpResponseRedirect(authorization_url)
       

# facebook login
class FacebookLogin(APIView):
    def get(self, request):
        # Construct the authorization URL
        facebook_auth_url = "https://www.facebook.com/v12.0/dialog/oauth"
        client_id = settings.FACEBOOK_APP_ID
        redirect_uri = 'http://localhost:8000/accounts/facebook/login/callback/'
        scope = 'email'  # Add additional scopes as needed
        state = 'random_state_value'

        authorization_url = f"{facebook_auth_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}"

        # Redirect the user to the authorization URL
        return HttpResponseRedirect(authorization_url)



class GoogleCallback(APIView):
    def get(self, request):
        # Handle Google callback and authenticate user
        if 'code' in request.GET:
            code = request.GET.get('code')
            # Exchange authorization code for access token
            token_endpoint = "https://oauth2.googleapis.com/token"
            client_id = settings.GOOGLE_CLIENT_ID  
            client_secret = settings.GOOGLE_CLIENT_SECRET  
            redirect_uri = 'http://localhost:8000/accounts/google/login/callback/'

            params = {
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }

            response = requests.post(token_endpoint, data=params)
            token_data = response.json()

            # Use the access token to get user info
            access_token = token_data.get('access_token')
            id_token_data = token_data.get('id_token')
            user_info_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo'
            headers = {'Authorization': f'Bearer {access_token}'}

            user_info_response = requests.get(user_info_endpoint, headers=headers)
            user_info = user_info_response.json()

            # Verify ID token
            idinfo = id_token.verify_oauth2_token(id_token_data, google_requests.Request(), client_id)

            # Check if the ID token is valid
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Invalid ID token issuer')

            # Authenticate or create the user
            email = user_info.get('email')
            first_name = user_info.get('given_name')
            last_name = user_info.get('family_name')
            user, created = User.objects.get_or_create(email=email, first_name=first_name, last_name=last_name)

            # Log in the user
            if created:
                user.save()

            # Generate token
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({"token": token.key, "message": "User created successfully."}, status=status.HTTP_201_CREATED)

        else:
            return Response({"message": "Authorization code not found."}, status=status.HTTP_400_BAD_REQUEST)


class FacebookCallback(APIView):
    def get(self, request):
        # Handle Facebook callback and authenticate user
        if 'code' in request.GET:
            code = request.GET.get('code')
            # Exchange authorization code for access token
            token_endpoint = "https://graph.facebook.com/v12.0/oauth/access_token"
            client_id = settings.FACEBOOK_APP_ID
            client_secret = settings.FACEBOOK_APP_SECRET
            redirect_uri = 'http://localhost:8000/accounts/facebook/login/callback/'

            params = {
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
            }

            response = requests.get(token_endpoint, params=params)
            token_data = response.json()

            # Use the access token to get user info
            access_token = token_data.get('access_token')
            user_info_endpoint = 'https://graph.facebook.com/v12.0/me?fields=id,email,first_name,last_name'
            user_info_params = {
                'access_token': access_token
            }

            user_info_response = requests.get(user_info_endpoint, params=user_info_params)
            user_info = user_info_response.json()

            # Authenticate or create the user
            email = user_info.get('email')
            first_name = user_info.get('first_name')
            last_name = user_info.get('last_name')
            user, created = User.objects.get_or_create(email=email, first_name=first_name, last_name=last_name)

            # Log in the user
            if created:
                user.save()

            # Generate token
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({"token": token.key, "message": "User created successfully."}, status=status.HTTP_201_CREATED)

        else:
            return Response({"message": "Authorization code not found."}, status=status.HTTP_400_BAD_REQUEST)

