from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=200)

    diaries: fields.ReverseRelation["Diary"]  # 관계 필드

class Diary(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    author = fields.ForeignKeyField("models.User", related_name="diaries")