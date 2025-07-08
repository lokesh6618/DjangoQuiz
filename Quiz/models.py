from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()


class Question(models.Model):
    uid        = models.CharField(max_length=20, unique=True)
    text       = models.TextField(blank=True, null=True)
    image      = models.ImageField(upload_to="math_2024_430_1_1_BASIC/", blank=True, null=True)
    year       = models.IntegerField(default=2024)
    paper_code = models.CharField(max_length=20, default="30-1-1")

    op1 = models.CharField(max_length=200)
    op2 = models.CharField(max_length=200)
    op3 = models.CharField(max_length=200)
    op4 = models.CharField(max_length=200)

    correct = models.PositiveSmallIntegerField(choices=[(1, "A"), (2, "B"), (3, "C"), (4, "D")])

    def __str__(self):
        return f"Q{self.uid} - {self.paper_code}"

class Choice(models.Model):
    """
    Four choices per question.  Exactly one should have is_correct=True.
    """
    question   = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    text       = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.id} – {self.text[:60]}"


class QuizAttempt(models.Model):
    """
    One row per quiz run.
    Only aggregates are stored; per‑question responses are optional.
    """
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at      = models.DateTimeField(auto_now_add=True)
    finished_at     = models.DateTimeField(null=True, blank=True)
    duration        = models.PositiveIntegerField(null=True, blank=True)  # seconds
    score           = models.PositiveSmallIntegerField(default=0)  # /20
    total_attempted = models.PositiveSmallIntegerField(default=0)
    correct         = models.PositiveSmallIntegerField(default=0)
    wrong           = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.user} – {self.score}/20 on {self.started_at:%d %b %Y %H:%M}"


class QuestionPaper(models.Model):
    """
    One row per paper – eg “Maths 2024 Standard (30‑1‑1)”.
    """
    name           = models.CharField(max_length=120, unique=True)
    duration_min   = models.PositiveSmallIntegerField(default=30)   # test length
    max_marks      = models.PositiveSmallIntegerField(default=20)
    subject        = models.CharField(max_length=50, default="Maths")

    def __str__(self):
        return self.name


class QuestionBank(models.Model):
    """
    Individual questions belonging to a paper.
    """
    paper            = models.ForeignKey(QuestionPaper,
                                         on_delete=models.CASCADE,
                                         related_name="questions")
    question_number  = models.PositiveSmallIntegerField()
    image_path       = models.CharField(max_length=255)
    answer           = models.CharField(max_length=100)   # flexible (int/float/str)
    marks = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ("paper", "question_number")
        ordering        = ["question_number"]

    def __str__(self):
        return f"{self.paper}  Q{self.question_number}"


class Teacher(models.Model):
    email      = models.EmailField(unique=True)
    teacher_id = models.CharField(max_length=30, unique=True)
    name       = models.CharField(max_length=100)
    password   = models.CharField(max_length=128)  # hashed

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Student(models.Model):
    teacher      = models.ForeignKey(Teacher, on_delete=models.CASCADE,
                                     related_name="students")
    student_id   = models.CharField(max_length=30)
    name         = models.CharField(max_length=100)
    # password     = models.CharField(max_length=128)  # optional / hashed

    class Meta:
        unique_together = ("teacher", "student_id")

    # def save(self, *args, **kwargs):
    #     if self.password and not self.password.startswith("pbkdf2_"):
    #         self.password = make_password(self.password)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} – {self.teacher.name}"


class TestResult(models.Model):
    """
    One sitting of one paper by one student.
    """
    student        = models.ForeignKey(Student, on_delete=models.CASCADE,
                                       related_name="results")
    paper          = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE,
                                       related_name="results")
    start_time     = models.DateTimeField()
    end_time       = models.DateTimeField()
    correct        = models.PositiveSmallIntegerField()
    incorrect      = models.PositiveSmallIntegerField()
    not_attempted  = models.PositiveSmallIntegerField()
    score          = models.DecimalField(max_digits=6, decimal_places=2)
    maximum_score  = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.student} – {self.paper} – {self.score}/{self.maximum_score}"
