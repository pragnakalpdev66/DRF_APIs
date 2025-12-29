from authentication.models import User
from rest_framework import serializers
from django.db import models
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'role', 'gender', 'date_of_birth', 'profile']
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at', 'is_deleted']

    def validate_role(self, value):
        if value not in ['user', 'admin']:
            raise serializers.ValidationError()
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            password = validated_data['password'],
            role = validated_data.get('role'),
            gender = validated_data.get('gender'),
            date_of_birth = validated_data.get('date_of_birth'),
            profile = validated_data.get('profile'),
        )
        if validated_data.get('role') == 'admin':
            user.is_staff = True
            user.save() 
        return user

class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        # uid = urlsafe_base64_encode(force_bytes(user.pk))
        uid = urlsafe_base64_encode(force_bytes(str(user.pk)))

        token = PasswordResetTokenGenerator().make_token(user)
        
        reset_link = f"http://127.0.0.1:8000/auth/reset-password/?uid={uid}&token={token}"

        return {
            "email": email,
            "uid": uid,
            "token": token,
            "reset_link": reset_link
        }

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            print("passwords do not match")
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def save(self):
        email = self.validated_data['email']
        uid = self.validated_data['uid']
        token = self.validated_data['token']
        new_password = self.validated_data['new_password']

        try:
            decoded_uid = urlsafe_base64_decode(uid).decode()
        except Exception:
            raise serializers.ValidationError("Invalid UID.")

        try:
            user = User.objects.get(email=email)
        except:
            raise serializers.ValidationError("User not found")
        
        try:
            user = User.objects.get(pk=decoded_uid)
        except:
            raise serializers.ValidationError("Invalid reset request.")

        
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Invalid or expired token.")

        user.set_password(new_password)
        user.save()

        return user
