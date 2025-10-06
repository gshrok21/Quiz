from django.contrib import admin
from answer.models import answer_list,scorecard
# Register your models here.
class admin_answers(admin.ModelAdmin):
    list_display=('attempted_by','quizid','questionid','chosen_option','answer','mark')
    
class admin_score(admin.ModelAdmin):
    list_display =('attempted_by','quizid', 'total','score','correct','incorrect')
    
admin.site.register(answer_list,admin_answers)
admin.site.register(scorecard, admin_score)