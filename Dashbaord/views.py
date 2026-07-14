from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.conf import settings
from Application.AuthenticationServices.auth_models import User
from Application.AuthenticationServices.auth_views import set_auth_cookies
from django.conf import settings

class AdminLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        identifier = request.data.get("identifier")
        password = request.data.get("password")


        if not identifier or not password:
            return Response(
                {"message": "Identifier and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(
            Q(username=identifier) | Q(email=identifier) | Q(phone=identifier)
        ).first()

        if not user or not user.check_password(password):
            return Response(
                {"message": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure the user has admin/staff privileges
        if not (user.is_superuser or user.is_staff):
            return Response(
                {"message": "You do not have permission to access the dashboard."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        response = Response({
            "message": "Login successful",
        }, status=status.HTTP_200_OK)

        # Set cookies
        set_auth_cookies(response, refresh)
        return response
    
class CheckLogin(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {"is_logined": True, "message": "You are logged in"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"is_logined": False, "message": "You are not logged in"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class Logout(APIView):
    def post(self, request):
        response = Response({
            "message": "Logout successful",
        }, status=status.HTTP_200_OK)
        
        samesite = getattr(settings, 'SIMPLE_JWT_COOKIE_SAMESITE', 'Lax')
        
        response.delete_cookie("access_token", samesite=samesite)
        response.delete_cookie("refresh_token", samesite=samesite)
        return response