from tortoise import Model
from tortoise.fields import CharField, DatetimeField


class RefreshTokenRecord(Model):
    class Meta:
        table = "refresh_token"

    id = CharField(primary_key=True, max_length=200)
    username = CharField(max_length=200)
    auth_at = DatetimeField()
    expires_at = DatetimeField()
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)
