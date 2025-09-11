from tortoise import fields, models
from tortoise.contrib.postgres.functions import Random
# ----------------------------
# Users (회원가입/로그인)
# ----------------------------
class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    password_hash = fields.CharField(max_length=255)
    nickname = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    diaries: fields.ReverseRelation["Diary"]

    # Relations
    diaries: fields.ReverseRelation["Diary"]
    bookmarks: fields.ReverseRelation["Bookmark"]
    tokens: fields.ReverseRelation["TokenBlacklist"]

    def __str__(self):
        return self.username

    @staticmethod
    async def get_random_quote():
        """DB에서 랜덤 명언 1개 반환"""
        from app.models import Quote
        return await Quote.all().order_by(Random()).first() #type: ignore




# ----------------------------
# Diaries (일기 작성 및 관리)
# ----------------------------
class Diary(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="diaries")
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.title


# ----------------------------
# Quotes (명언)
# ----------------------------
class Quote(models.Model):
    id = fields.IntField(pk=True)
    quote_content = fields.TextField()
    author = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)


    # Relations
    bookmarks: fields.ReverseRelation["Bookmark"]

    def __str__(self):
        return f"{self.author}: {self.quote_content[:30]}"

    async def is_bookmarked_by(self, user: "User"):
        return await Bookmark.exists(user=user, quote=self)
# ----------------------------
# Bookmarks (명언 북마크)
# ----------------------------
class Bookmark(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="bookmarks")
    quote = fields.ForeignKeyField("models.Quote", related_name="bookmarks")
    created_at = fields.DatetimeField(auto_now_add=True)


# ----------------------------
# Token_blacklist (로그아웃된 JWT 토큰 저장)
# ----------------------------
class TokenBlacklist(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="tokens")
    token = fields.CharField(max_length=512)
    expired_at = fields.DatetimeField()
    created_at = fields.DatetimeField(auto_now_add=True)


# ----------------------------
# Question (자기성찰 질문)
# ----------------------------
class Question(models.Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()
    category = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:30]
