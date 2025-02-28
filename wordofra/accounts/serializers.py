from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import NewsletterSubscriber
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ('email', 'name')

class NewsletterUnsubscribeSerializer(serializers.Serializer):
    email = serializers.EmailField()


# JWT Token customization

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print("ARE WE GETTING HERE?")
        token = super().get_token(user)
        token["username"] = user.username  # Add username to the token
        return token