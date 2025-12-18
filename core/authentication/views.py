from rest_framework import generics, views, status
from authentication.serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .serializers import ForgotPasswordSerializer , ResetPasswordSerializer
from django.core.mail import send_mail

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):

        user = serializer.save()
        print(f"{user} registration succesfull!!")
        return user
    
# class LoginView(APIView):
#     serializer_class = UserLoginSerializer

#     def post(self, request, *args, **kwargs):
#         print(request.data)
#         # serializer = self.get_serializer(data=request.data)
#         serializer = UserLoginSerializer(data=request.data)
#         if not serializer.is_valid():
#             print(serializer.errors)
#             print("not valid")
#             # return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']
#         # print(email, password)
#         user = authenticate(request, email=email, password=password)
#         print(user)

#         if user is not None:
#             refresh = RefreshToken.for_user(user)

#             return Response({
#                 "message": "Login successful!!",
#                 'email': user.email,
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 "detail": "Invalid Credentials..!!"
#             }, status=status.HTTP_401_UNAUTHORIZED)
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
