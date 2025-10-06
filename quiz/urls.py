"""
URL configuration for quiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from quiz import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup',views.signup),
    path('login_page',views.login_page),
    path("",views.dashboard),
    path('logout_page',views.logout_page),
    path('create_quiz',views.create_quiz),
    path('my_quizzes',views.my_quizzes),
    path('questionlist/',views.questionlist),
    path('attempt_quiz',views.attempt_quiz),
    path('submit_quiz',views.submit_quiz),
    path('answerlist/',views.answerlist),
    path('attempted_quizzes',views.attempted_quizzes),
    path('scorecard',views.calc_score),
    path('responselist',views.responselist),
    path('view_response/',views.view_response),
    path('view_response/user_response/',views.user_response)
]
