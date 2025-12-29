from rest_framework import generics, views, status
from authentication.serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework.response import Response
from .serializers import ForgotPasswordSerializer , ResetPasswordSerializer
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):

        user = serializer.save()
        print(f"{user} registration succesfull!!")
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "user_updates",
                {
                    "type": "send_notification", 
                    "message": {
                        "event": "NEW USER REGISTERED",
                        "username": f"{user.first_name} {user.last_name}",
                        "email": user.email,
                        "role": user.role,
                        "timestamp": "2025-12-24"
                    }
                }
            )
        except Exception as e:
            print(f"WebSocket Notification Failed: {e}")
        return user
 
class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

class ForgotPasswordAPIView(APIView):

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()

            print(f"data: {data}")

            send_mail(
                subject="Reset Your Password",
                message=f"Click the link to reset your password:\n{data['reset_link']}",
                from_email=None,
                recipient_list=[data['email']],
            )
            
            return Response({
                "message": "Password reset instructions sent",
                "email": data["email"],
                "uid": data["uid"],
                "token": data["token"],
                "reset_link": data["reset_link"]
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(APIView):

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        print("Request Data:", request.data)
        if serializer.is_valid():
            serializer.save()

            print("Password reset executed successfully!")
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

