from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators  import login_required
from django.shortcuts import render,redirect
from django.contrib import messages 
from django.http import HttpResponse
from question.models import question_list
from answer.models import answer_list,scorecard
def signup(request):
    if request.method =="POST":
        username=request.POST.get("username")
        fname=request.POST.get("fname")
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exist")
        elif password1 ==password2:
            myuser=User.objects.create_user(username=username,password=password1, email=email,first_name=fname)
            myuser.save()
            messages.success(request,"Registered Successfully")
            return redirect("/login_page")
        else:
            messages.error(request,"Password does not match")
    return render(request, "signup.html")
    
def login_page(request):
    if request.method =="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            messages.error(request, "username invalid")
        else:
            myuser=authenticate(username=username, password=password)
            if myuser is None:
                messages.error(request,"Invalid Password")
            else:
                login(request, myuser)
                return render(request, "dashboard.html")
            
    return render(request, "login.html")

def dashboard(request):
    return render(request, "dashboard.html")
    
def logout_page(request):
    logout(request)
    return render( request, "dashboard.html")

@login_required 
def create_quiz(request):
    #quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        # Get list of all question fields
        username=str(request.user.username)
        quizid =request.POST.get('quizid')
        questions = request.POST.getlist('question')
        option1s = request.POST.getlist('op1')
        option2s = request.POST.getlist('op2')
        option3s = request.POST.getlist('op3')
        option4s = request.POST.getlist('op4')
        correct_options = request.POST.getlist('correct_option')
        marks = request.POST.getlist('mark')

        # Loop and create questions
        for i in range(len(questions)):
            question_list.objects.create(
                username=username,
                quizid=quizid,
                questionid=quizid+str(i),
                question=questions[i],
                op1=option1s[i],
                op2=option2s[i],
                op3=option3s[i],
                op4=option4s[i],
                correct_option=correct_options[i],
                mark=marks[i]
            )
        return redirect('/')
    return render(request, 'create_quiz.html')
@login_required   
def my_quizzes(request):
    result=question_list.objects.filter(username=str(request.user.username)).values('quizid').distinct()
    return render(request,'my_quizzes.html',{"result":result})
@login_required
def attempted_quizzes(request):
    result1=answer_list.objects.filter(attempted_by=str(request.user.username)).values('quizid').distinct()
    result2=scorecard.objects.filter(attempted_by=str(request.user.username))
    return render(request,'attempted_quizzes.html',{"result1":result1,'result2':result2})
@login_required
def answerlist(request):
    if request.method =="GET":
        quizid=request.GET.get("quizid")
        data1=question_list.objects.filter(quizid=quizid)
        data2=answer_list.objects.filter(quizid=quizid,attempted_by=str(request.user.username))
        return render(request,'answerlist.html',{"data1":data1,'data2':data2})
    return render(request,"answerlist.html")
    
@login_required 
def questionlist(request):
    if request.method =="GET":
        quizid=request.GET.get("quizid")
        data=question_list.objects.filter(quizid=quizid)
        print(data)
        return render(request,'questionlist.html',{"data":data})
    return render(request,"questionlist.html")
 
@login_required  
def attempt_quiz(request):
    if request.method =='POST':
        request.session.pop('quizid',None)
        quizid=request.POST.get("quizid")
        request.session['quizid']=quizid
        
        if scorecard.objects.filter(quizid =quizid, attempted_by =str(request.user.username)).exists():
            messages.error(request, "You Already Attempted This Quiz")
        else:
            result=question_list.objects.filter(quizid=quizid)
            return render(request,"attemp_quiz.html",{'result':result})
    return render(request,"attemp_quiz.html")

@login_required   
def submit_quiz(request):
    score=0
    if request.method =='POST':
        username=str(request.user.username)
        quizid=request.session.get("quizid")
        for key,value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                result=question_list.objects.filter(questionid=key)
                ans=""
                for i in list(result):
                    ans=i.correct_option
                    scr=i.mark
                answer_list.objects.create(attempted_by=username, quizid=quizid, questionid=key,chosen_option=value, answer=ans,mark=scr)
    return redirect('/scorecard')

@login_required  
def calc_score(request):
    score=0
    total=0
    correct=0
    incorrect=0
    tn=0
    quizid=request.session.get("quizid")
    dataset=answer_list.objects.filter(quizid=quizid,attempted_by=str(request.user.username))
    for a in list(dataset):
        if a.chosen_option==a.answer:
            score+=a.mark
            correct+=1
        total+=a.mark
        tn+=1
        incorrect=tn-correct
    data=scorecard.objects.filter(quizid=quizid,attempted_by=str(request.user.username))
    if not data.exists():
        scorecard.objects.create(score=score, total=total,correct=correct,incorrect=incorrect,attempted_by=str(request.user.username),quizid=quizid)
        data=scorecard.objects.filter(quizid=quizid,attempted_by=str(request.user.username))
        return render(request,'scorecard.html',{'data':data})
    return render(request,'scorecard.html',{'data':data})

@login_required   
def responselist(request):
    result=question_list.objects.filter(username=str(request.user.username)).values('quizid').distinct()
    return render(request,'responselist.html',{"result":result})

@login_required  
def view_response(request):
    if request.method =="GET":
        quizid=request.GET.get("quizid")
        data=scorecard.objects.filter(quizid=quizid)
        return render(request,'view_response.html',{"data":data})
    return render(request,'view_response.html')

@login_required   
def user_response(request):
    if request.method == "GET":
        quizid =request.GET.get("quizid")
        username=request.GET.get("user")
        data1=question_list.objects.filter(quizid=quizid)
        data2=answer_list.objects.filter(quizid=quizid,attempted_by=username)
        return render(request,'user_response.html',{"data1":data1,'data2':data2})
    return render(request,"user_response.html")
        