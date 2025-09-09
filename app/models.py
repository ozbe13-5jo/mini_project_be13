from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(primary_key=True)
    email = fields.CharField(max_length=255, unique=True, db_index=True)
    password_hash = fields.CharField(max_length=255)
    nickname = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    token_blacklist: fields.ReverseRelation["TokenBlacklist"]

    class Meta:
        table = "users"


class TokenBlacklist(Model):
    id = fields.IntField(primary_key=True)
    token = fields.CharField(max_length=1000, unique=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="token_blacklist", on_delete=fields.CASCADE, null=True
    )
    expired_at = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "token_blacklist"

__all__ = ["User", "TokenBlacklist"]
