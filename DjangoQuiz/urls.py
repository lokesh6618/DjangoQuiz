from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Quiz import views           # import the functions we just rewrote
from django.conf import settings
from django.conf.urls.static import static
from Quiz.views import (
    TeacherViewSet, StudentViewSet,
    QuestionPaperViewSet, QuestionBankViewSet, TestResultViewSet,
    home, start_quiz, submit_quiz, result,
)

# DjangoQuiz/urls.py   (project‑level)
router = DefaultRouter()
router.register("teachers",  TeacherViewSet)
router.register("students",  StudentViewSet)
router.register("papers",    QuestionPaperViewSet)
router.register("questions", QuestionBankViewSet)
router.register("results",   TestResultViewSet)

urlpatterns = [
    # ── Admin ───────────────────────────────────────────────
    path("admin/", admin.site.urls),

    # ── Landing / dashboard ─────────────────────────────────
    path("", home, name="home"),

    # ── Quiz flow ───────────────────────────────────────────
    path("quiz/start/",  start_quiz,  name="start_quiz"),
    path("quiz/submit/", submit_quiz, name="submit_quiz"),
    path("quiz/result/<int:attempt_id>/", result, name="result"),

    # ── Authentication ─────────────────────────────────────
    path("register/", views.register_page, name="register"),
    path("login/",    views.login_page,    name="login"),
    path("logout/",   views.logout_page,   name="logout"),

    # REST API
    # ── REST API ─────────────────────────────────────
    path("api/", include(router.urls)),

    # (Optional) manual question‑adder view, keep only if you still need it:
    # path("add-question/", views.add_question, name="add_question"),
]

# ── Media / static in DEBUG ────────────────────────────────
if settings.DEBUG:                        # serve uploads in dev only
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
