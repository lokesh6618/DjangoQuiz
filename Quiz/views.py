# views.py
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

from .models import (
    Teacher, Student, QuestionPaper, QuestionBank, Question, Choice, QuizAttempt, TestResult
)
from .viewsets import (
    TeacherViewSet,
    StudentViewSet,
    QuestionPaperViewSet,
    QuestionBankViewSet,
    TestResultViewSet,
)

# 1.  Landing page ────────────────────────────────────────────────────────────
def home(request):
    """
    Landing page listing all available papers for the drop‑down.
    Assumes the logged‑in user is a Teacher (or staff).
    """
    papers = QuestionPaper.objects.all()
    return render(request, "Quiz/home.html", {"papers": papers})


# 2.  Register / Login / Logout ──────────────────────────────────────────────
def register_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)               # auto‑login after sign‑up
        return redirect("home")

    return render(request, "Quiz/register.html", {"form": form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("home")

    return render(request, "Quiz/login.html", {"form": form})


@login_required
def logout_page(request):
    logout(request)
    return redirect("home")


# 3.  Quiz flow ──────────────────────────────────────────────────────────────
@login_required
def start_quiz(request):
    """
    GET params:
      ?paper=<paper_id>&student=<student_name>
    Creates Student (if needed) and a TestResult row, then renders quiz page.
    """
    
    # print("request : ", request)
    
    paper_id     = request.GET.get("paper") or request.GET.get("question_paper_id")
    # print("paper_id : ", paper_id)
    
    student_name = request.GET.get("student", "").strip() or request.GET.get("student_name", "").strip()
    # print("student_name : ", student_name)
    
    if not paper_id or not student_name:
        return redirect("home")

    paper     = get_object_or_404(QuestionPaper, id=paper_id)
    questions = paper.questions.all()[:paper.max_marks]

    # Map auth user to teacher
    teacher = Teacher.objects.filter(email=request.user.email).first()
    if not teacher:
        teacher = Teacher.objects.create(
            email=request.user.email,
            teacher_id=f"AUTH-{request.user.id}",
            name=request.user.get_full_name() or request.user.username,
            password="unused"
        )

    # Ensure student exists
    student, _ = Student.objects.get_or_create(
        teacher=teacher,
        student_id=student_name.replace(" ", "").lower(),
        defaults={"name": student_name}
    )

    # Create a test attempt
    attempt = TestResult.objects.create(
        student=student,
        paper=paper,
        start_time=timezone.now(),
        end_time=timezone.now(),  # will update later
        correct=0,
        incorrect=0,
        not_attempted=0,
        score=0,
        maximum_score=paper.max_marks,
    )

    request.session["attempt_id"] = attempt.id

    return render(request, "Quiz/quiz.html", {
        "questions": questions,
        "paper": paper,
        "question_paper": paper,
        "student_name": student.name,
    })

@login_required
def submit_quiz(request):
    """
    Handles POST from quiz.html (manual submit or auto‑submit after 30 min).
    Calculates score, updates QuizAttempt, and redirects to result page.
    """
    if request.method != "POST":
        return redirect("home")

    attempt_id = request.session.pop("attempt_id", None)
    if not attempt_id:
        return HttpResponse("No active attempt.", status=400)

    attempt   = get_object_or_404(TestResult, id=attempt_id)
    questions = attempt.paper.questions.all()

    total_attempted = correct = 0
    for q in questions:
        val = request.POST.get(f"q{q.id}")
        if not val:  # empty
            continue
        total_attempted += 1
        if val.strip() == q.answer.strip():
            correct += 1

    attempt.correct        = correct
    attempt.incorrect      = total_attempted - correct
    attempt.not_attempted  = len(questions) - total_attempted
    attempt.score          = correct                  # 1 mark each
    attempt.end_time       = timezone.now()
    attempt.save()

    return redirect("result", attempt_id=attempt.id)


@login_required
def result(request, attempt_id):
    attempt = get_object_or_404(TestResult, id=attempt_id)
    percent = attempt.score / attempt.maximum_score * 100
    return render(request, "Quiz/result.html", {
        "attempt": attempt,
        "score": attempt.score,
        "percent": round(percent, 2),
        "time": int((attempt.end_time - attempt.start_time).total_seconds()),
        "correct": attempt.correct,
        "wrong": attempt.incorrect,
        "total": attempt.maximum_score,
    })
