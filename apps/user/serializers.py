from rest_framework import serializers

from apps.user.models import User


class UserRegistrationInputSerializer(serializers.Serializer):
    password = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)


class CheckLoginTypeInputSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)


class UserLoginInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    type = serializers.ChoiceField(choices=(('password', 'password'), ('otp', 'otp')))
    pass_code = serializers.CharField()


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class CheckLoginTypeOutputSerializer(serializers.Serializer):
    username = serializers.CharField()
    type = serializers.ChoiceField(choices=(('password', 'password'), ('otp', 'otp')))


class LoginOutputSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
