from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.get_username()
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            "user": {
                "id": self.user.id,
                "username": self.user.get_username(),
                "email": self.user.email,
            }
        })
        return data
