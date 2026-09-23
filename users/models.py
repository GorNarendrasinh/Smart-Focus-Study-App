
from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    mobile = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.CharField(
        max_length=255
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.text


class JournalEntry(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.content[:50]


class TimetableTask(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.CharField(
        max_length=255
    )

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.text


class UserActivity(models.Model):

    ACTIVITY_TYPES = [
        ("page_view", "Page View"),
        ("study_start", "Study Started"),
        ("study_stop", "Study Stopped"),
        ("task_add", "Task Added"),
        ("task_complete", "Task Completed"),
        ("task_delete", "Task Deleted"),
        ("note_save", "Note Saved"),
        ("note_delete", "Note Deleted"),
        ("mission", "Mission Locked"),
        ("mood", "Mood Updated"),
        ("pomodoro_start", "Pomodoro Started"),
        ("pomodoro_complete", "Pomodoro Completed"),
        ("login", "Login"),
        ("logout", "Logout"),
        ("timetable_add", "Timetable Added"),
        ("timetable_complete", "Timetable Completed"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="study_activities"
    )

    activity_type = models.CharField(
        max_length=50,
        choices=ACTIVITY_TYPES,
        default="other"
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        default=""
    )

    subject = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    duration_seconds = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"

