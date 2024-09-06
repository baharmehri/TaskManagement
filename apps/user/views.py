from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound

from apps.core.exceptions import DuplicatedError, InvalidPassCode
from apps.core.response import CustomResponse as response
from apps.user.serializers import UserRegistrationInputSerializer, UserOutputSerializer, \
    CheckLoginTypeInputSerializer, UserLoginInputSerializer
from apps.user.services import UserService


class RegisterView(APIView):
    @extend_schema(
        request=UserRegistrationInputSerializer
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
        request=CheckLoginTypeInputSerializer
    )
    def post(self, request):
        data = CheckLoginTypeInputSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        try:
            result = UserService().check_login_type(data.data)
        except NotFound as e:
            return response.error_response(str(e), status.HTTP_400_BAD_REQUEST)

        return response.data_response(data=result, message="check login type successfully", status=status.HTTP_200_OK)


class LoginView(APIView):
    @extend_schema(
        request=UserLoginInputSerializer
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

        return response.data_response(data=tokens, message="login successfully", status=status.HTTP_200_OK)
