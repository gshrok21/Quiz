from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators  import login_required
from django.shortcuts import render,redirect
from django.contrib import messages 
from django.http import HttpResponse
from quizid.models import QuizID
from question.models import question_list
from answer.models import answer_list,scorecard
from django.db import transaction
def signup(request):
    with transaction.atomic():
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
            messages.error(request, "invalid credentials")
        else:
            myuser=authenticate(username=username, password=password)
            if myuser is None:
                messages.error(request,"Invalid credentials")
            else:
                login(request, myuser)
               
                return redirect("/")
            
    return render(request, "login.html")

def dashboard(request):
    return render(request, "dashboard.html")
    
def logout_page(request):
    logout(request)
    return render( request, "dashboard.html")

@login_required
def create_quiz(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                # Get list of all question fields
                username=request.user
                quizid =request.POST.get('quizid')
                quiz, _ = QuizID.objects.get_or_create(
                    quiz_id=quizid,
                    creator=request.user,
                )

                questions = request.POST.getlist('question')
                option1s = request.POST.getlist('op1')
                option2s = request.POST.getlist('op2')
                option3s = request.POST.getlist('op3')
                option4s = request.POST.getlist('op4')
                correct_options = request.POST.getlist('correct_option')
                marks = request.POST.getlist('mark')

                # Loop and create questions
                qlist=[]
                for i in range(len(questions)):
                        qlist.append(question_list(
                        username=username,
                        quiz_id=quiz,
                        questionid=quizid+str(i),
                        question=questions[i],
                        op1=option1s[i],
                        op2=option2s[i],
                        op3=option3s[i],
                        op4=option4s[i],
                        correct_option=correct_options[i],
                        mark=marks[i]))
                question_list.objects.bulk_create(qlist)
                    
                return redirect('/')
            return render(request, 'create_quiz.html')
    except Exception as e:
        print('error',e)
        return HttpResponse("error - " + str(e))

@login_required   
def my_quizzes(request):
    result=QuizID.objects.filter(creator=request.user)
    return render(request,'my_quizzes.html',{"result":result})
@login_required
def attempted_quizzes(request):
    result1=answer_list.objects.filter(attempted_by=request.user).values('quiz_id').distinct()
    result2=scorecard.objects.filter(attempted_by=request.user).select_related('quiz_id')
    return render(request,'attempted_quizzes.html',{"result1":result1,'result2':result2})
@login_required
def answerlist(request):
    if request.method =="GET":
        quizid=request.GET.get("quizid")
        data2=answer_list.objects.select_related('questionid').filter(
            quiz_id=quizid,
            attempted_by=request.user,
        )
        return render(request,'answerlist.html',{'data2':data2})
    return render(request,"answerlist.html")
    
@login_required 
def questionlist(request):
    if request.method =="GET":
        quizid=request.GET.get("quizid")
        data=question_list.objects.filter(quiz_id_id=quizid)
        return render(request,'questionlist.html',{"data":data})
    return render(request,"questionlist.html")
 
@login_required  
def attempt_quiz(request):
    if request.method =='POST':
        request.session.pop('quizid',None)
        quizid=request.POST.get("quizid")
        quizid=QuizID.objects.get(quiz_id=quizid)
        print('quizid',quizid.pk)
        request.session['quizid']=quizid.quiz_id
        
        if scorecard.objects.filter(quiz_id=quizid.quiz_id, attempted_by=request.user).exists():
            messages.error(request, "You Already Attempted This Quiz")
        else:
            result=question_list.objects.filter(quiz_id=quizid.pk)
            return render(request,"attemp_quiz.html",{'result':result})
    return render(request,"attemp_quiz.html")

@login_required   
def submit_quiz(request):
    if request.method =='POST':
        quizid=request.session.get("quizid")
        QuizInst=QuizID.objects.get(quiz_id=quizid)
        for key,value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                question=question_list.objects.get(questionid=key)
                answer_list.objects.create(
                    attempted_by=request.user,
                    quiz_id=QuizInst,
                    questionid=question,
                    chosen_option=value,
                    answer=question.correct_option,
                    mark=question.mark,
                )
    return redirect('/scorecard')

@login_required  
def calc_score(request):
    score=0
    total=0
    correct=0
    incorrect=0
    tn=0
    quizid=request.session.get("quizid")
    QuizInst=QuizID.objects.get(quiz_id=quizid)
    
    data=scorecard.objects.filter(quiz_id=QuizInst,attempted_by=request.user)
    if not data.exists():
        dataset=answer_list.objects.filter(quiz_id=QuizInst,attempted_by=request.user)
        for a in list(dataset):
            if a.chosen_option==a.answer:
                score+=a.mark
                correct+=1
            total+=a.mark                
            tn+=1
            incorrect=tn-correct
        scorecard.objects.get_or_create(
            score=score,
            total=total,
            correct=correct,
            incorrect=incorrect,
            attempted_by=request.user,
            quiz_id=QuizInst,
        )
        return render(request,'scorecard.html',{'data':data})
    return render(request,'scorecard.html',{'data':data})

@login_required   
def responselist(request):
    result=QuizID.objects.filter(creator=request.user).values('quiz_id')
    return render(request,'responselist.html',{"result":result})

@login_required  
def view_response(request):
    if request.method =="GET":
        quizid=request.GET.get("quizid")
        data=scorecard.objects.filter(quiz_id=quizid)
        return render(request,'view_response.html',{"data":data})
    return render(request,'view_response.html')

@login_required   
def user_response(request):
    if request.method == "GET":
        quizid =request.GET.get("quizid")
        username=request.GET.get("user")
        data1=question_list.objects.filter(quiz_id__quiz_id=quizid)
        data2=answer_list.objects.filter(
            quiz_id=quizid,
            attempted_by__username=username,
        ).select_related('questionid')
        return render(request,'user_response.html',{"data1":data1,'data2':data2})
    return render(request,"user_response.html")
        