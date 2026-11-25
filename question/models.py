from django.db import models
from django.contrib.auth.models import User
from quizid.models import QuizID
# Create your models here.
class question_list(models.Model):
    username = models.ForeignKey(User,max_length=100,on_delete=models.CASCADE)
    quiz_id=models.ForeignKey(QuizID,max_length=100,db_index=True,on_delete=models.CASCADE)
    question=models.TextField()
    questionid=models.CharField(max_length=20,unique=True,null=False)
    op1=models.CharField(max_length=200)
    op2=models.CharField(max_length=200)
    op3=models.CharField(max_length=200)
    op4=models.CharField(max_length=200)
    options=[('op1','option 1'),('op2','option 2'),('op3','option 3'),('op4','option 4')]
    correct_option=models.CharField(max_length=100,choices=options)
    mark=models.IntegerField()
    
    def __str__(self):
        return self.question