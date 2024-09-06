from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.core.exceptions import DuplicatedError, InvalidPassCode
from apps.core.response import CustomResponse as response
from apps.user.serializers import UserRegistrationInputSerializer, UserOutputSerializer, \
    CheckLoginTypeInputSerializer, UserLoginInputSerializer, CheckLoginTypeOutputSerializer, LoginOutputSerializer, \
    SendOtpInputSerializer
from apps.user.services import UserService


class RegisterView(APIView):
    @extend_schema(
        request=UserRegistrationInputSerializer,
        summary="Register a new user",
        description="This endpoint allows you to register a new user.",
        responses=UserOutputSerializer
    )
    def post(self, request):
        data = UserRegistrationInputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            user = UserService.register_user(data.data)
        except DuplicatedError as e:
            return response.error_response(e.message, status.HTTP_400_BAD_REQUEST)

        return response.data_response(data=UserOutputSerializer(user).data, message="register successfully",
                                      status=status.HTTP_200_OK)


class CheckLoginTypeView(APIView):
    @extend_schema(
        request=CheckLoginTypeInputSerializer,
        summary="Check the login type",
        description="This endpoint allows you to check the login type.",
        responses=CheckLoginTypeOutputSerializer
    )
    def post(self, request):
        data = CheckLoginTypeInputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            result = UserService().check_login_type(data.data)
        except NotFound as e:
            return response.error_response(str(e), status.HTTP_400_BAD_REQUEST)

        return response.data_response(data=CheckLoginTypeOutputSerializer(result).data,
                                      message="check login type successfully", status=status.HTTP_200_OK)


class LoginView(APIView):
    @extend_schema(
        request=UserLoginInputSerializer,
        summary="Login a user",
        description="This endpoint allows you to login a user.",
        responses=LoginOutputSerializer
    )
    def post(self, request):
        data = UserLoginInputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            tokens = UserService().login(data.data)
        except NotFound as e:
            return response.error_response(str(e), status.HTTP_400_BAD_REQUEST)
        except InvalidPassCode as e:
            return response.error_response(e.message, status.HTTP_400_BAD_REQUEST)

        return Response(LoginOutputSerializer(tokens).data, status=status.HTTP_200_OK)


class SendOtpView(APIView):
    @extend_schema(
        request=SendOtpInputSerializer,
        summary="Send OTP",
        description="This endpoint allows you to send an OTP.",
    )
    def post(self, request):
        data = SendOtpInputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            UserService.otp_sender(data.data)
        except Exception:
            return response.error_response("An internal error occurred.", status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response.data_response({}, "send otp successfully", status=status.HTTP_200_OK)
