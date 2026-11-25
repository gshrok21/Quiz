from django.contrib import admin
from .models import QuizID
# Register your models here.

class quizidadmin(admin.ModelAdmin):
    list_display=("quiz_id","creator")

admin.site.register(QuizID,quizidadmin)