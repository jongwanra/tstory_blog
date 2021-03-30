from django.db import models
from helpers.models import BaseModel
from users.models import User
from taggit.managers import TaggableManager
# Create your models here.


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    tags = TaggableManager()

    # admin 화면에서 object로만 보이는 것을 수정해줌
    def __str__(self):
        return "%s - %s - %s" % (self.user, self.id, self.title)

    def total_likes(self):
        return self.likes.count()


class Comment(BaseModel):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return "%s - %s" % (self.id, self.user)
