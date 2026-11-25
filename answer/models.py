from django.db import models
from django.contrib.auth.models import User
from quizid.models import QuizID
from question.models import question_list
# Create your models here.
class answer_list(models.Model):
    attempted_by=models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_id=models.ForeignKey(QuizID,to_field='quiz_id', on_delete=models.CASCADE)
    questionid=models.ForeignKey(question_list,to_field='questionid', on_delete=models.CASCADE)
    chosen_option=models.CharField(max_length =100)
    answer=models.CharField(max_length =100)
    mark=models.IntegerField()
class scorecard(models.Model):
    attempted_by=models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_id=models.ForeignKey(QuizID,to_field='quiz_id', on_delete=models.CASCADE)
    correct=models.IntegerField()
    incorrect=models.IntegerField()
    total=models.IntegerField()
    score=models.IntegerField()