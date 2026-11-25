from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class QuizID(models.Model):
    quiz_id=models.CharField(max_length=20,unique=True,null=False)
    creator=models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        unique_together=("quiz_id","creator")