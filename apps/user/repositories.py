from apps.base.repository import BaseRepository
from apps.user.models import User


class UserRepository(BaseRepository):
    model = User

    @classmethod
    def create_user(cls, email, username, password):
        return cls.model.objects.create_user(email=email, username=username, password=password)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.model.objects.filter(username=username).first()

    @classmethod
    def activate_user(cls, user: User):
        user.is_active = True
        user.save()
        return user
