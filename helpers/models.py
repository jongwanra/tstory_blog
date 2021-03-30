from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # 추상 클래스로 BaseModel 클래스를 사용하기 위함
    class Meta:
        abstract = True
