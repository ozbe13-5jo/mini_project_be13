from tortoise import fields, models
from app.models.models import User

class Diary(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    user = fields.ForeignKeyField("models.User", related_name="diaries")

    class Meta:
        table = "diaries"
