import re

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


class SendOtpInputSerializer(serializers.Serializer):
    recipient = serializers.CharField(required=True)
    type = serializers.ChoiceField(choices=(('email', 'email'), ('sms', 'sms')))
    username = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, data):
        if data['type'] == 'email':
            email = data['recipient']
            if not self.is_valid_email(email):
                raise serializers.ValidationError('Invalid email format.')
        if data['type'] == 'sms':
            number = data['recipient']
            if not self.is_valid_phone_number(number):
                raise serializers.ValidationError('Invalid phone number format.')
        return data

    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def is_valid_phone_number(self, number):
        phone_regex = '^09\d{9}$'
        if not re.match(phone_regex, number):
            raise serializers.ValidationError("Invalid phone number")
        return number


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
