from django.db import models

# Create your models here.
class answer_list(models.Model):
    attempted_by=models.CharField(max_length =100)
    quizid=models.CharField(max_length =100)
    questionid=models.CharField(max_length =100)
    chosen_option=models.CharField(max_length =100)
    answer=models.CharField(max_length =100)
    mark=models.IntegerField()
class scorecard(models.Model):
    attempted_by=models.CharField(max_length =100)
    quizid=models.CharField(max_length =100)
    correct=models.IntegerField()
    incorrect=models.IntegerField()
    total=models.IntegerField()
    score=models.IntegerField()