from abc import ABC, abstractmethod

from django.db import IntegrityError
from django.core.cache import cache
from django.contrib.auth.hashers import check_password

from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User
from apps.user.repositories import UserRepository
from apps.user.celery_tasks import send_otp
from apps.core.exceptions import DuplicatedError, InvalidPassCode


class AuthStrategy(ABC):
    @abstractmethod
    def validate(self, user, pass_code) -> bool:
        pass


class OTPAuthStrategy(AuthStrategy):
    def validate(self, user, pass_code) -> bool:
        try:
            pass_code = int(pass_code)
        except ValueError:
            raise InvalidPassCode()
        code = cache.get(user.pk)
        if not code:
            raise InvalidPassCode()
        if code != pass_code:
            return False
        cache.delete(user.pk)
        return True


class PasswordAuthStrategy(AuthStrategy):
    def validate(self, user, pass_code) -> bool:
        return check_password(password=pass_code, encoded=user.password)


class UserService:
    @staticmethod
    def _get_tokens(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return tokens

    @staticmethod
    def _get_user_by_username(username) -> User:
        user = UserRepository.get_user_by_username(username)
        if not user:
            raise NotFound("User not found")
        return user

    @staticmethod
    def register_user(validated_data: dict) -> User:
        try:
            user = UserRepository.create_user(
                email=validated_data["email"],
                username=validated_data["username"],
                password=validated_data.get("password"),
            )
        except IntegrityError as e:
            if 'user_user_username' in str(e):
                raise DuplicatedError("Username already exists")
            elif 'user_user_email' in str(e):
                raise DuplicatedError("Email already exists")

        return user

    def check_login_type(self, validated_data: dict) -> dict:
        user = self._get_user_by_username(validated_data["username"])
        login_type = {
            "username": user.username,
            "type": None
        }
        if user.password:
            login_type.update({"type": "password"})
            return login_type

        login_type.update({"type": "otp"})
        return login_type

    @staticmethod
    def resolve_auth(auth_type) -> AuthStrategy:
        obj = {
            'otp': OTPAuthStrategy(),
            'password': PasswordAuthStrategy()
        }
        return obj[auth_type]

    def login(self, validated_data: dict):
        user = self._get_user_by_username(validated_data["username"])

        auth = self.resolve_auth(validated_data["type"])
        validated_pass = auth.validate(user, validated_data["pass_code"])

        if not validated_pass:
            raise InvalidPassCode()

        tokens = self._get_tokens(user)
        return tokens

    @staticmethod
    def otp_sender(validated_data):
        user = validated_data["username"]
        recipient = validated_data["recipient"]
        send_otp.delay(user, recipient)
