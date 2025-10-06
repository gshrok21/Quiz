from django.contrib import admin
from question.models import question_list

# Register your models here.
class admin_quizlist(admin.ModelAdmin):
    list_display=('username', 'quizid','question')
    

    
admin.site.register(question_list,admin_quizlist)
