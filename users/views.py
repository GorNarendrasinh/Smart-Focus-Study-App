
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

from .models import (
    Account,
    Task,
    JournalEntry,
    TimetableTask,
    UserActivity,
)

# -------------------------
# Registration
# -------------------------
def registartion(request):

    if request.user.is_authenticated:
        return redirect("homePage")

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        mobile = request.POST.get("mobile", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not name or not email or not mobile or not password or not confirm_password:
            messages.error(request, "Please fill all fields.")
            return redirect("registartion")

        if not mobile.isdigit() or len(mobile) != 10:
            messages.error(
                request,
                "Please enter a valid 10-digit mobile number."
            )
            return redirect("registartion")

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return redirect("registartion")

        if len(password) < 6:
            messages.error(
                request,
                "Password must be at least 6 characters."
            )
            return redirect("registartion")

        if User.objects.filter(email__iexact=email).exists():
            messages.error(
                request,
                "Email is already registered."
            )
            return redirect("registartion")

        if Account.objects.filter(email__iexact=email).exists():
            messages.error(
                request,
                "Account already exists."
            )
            return redirect("registartion")

        # Create username from name
        base_username = name.lower().replace(" ", "")

        username = base_username
        counter = 1

        while User.objects.filter(username__iexact=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )

        Account.objects.create(
            name=name,
            email=email,
            mobile=mobile
        )

        messages.success(
            request,
            f"Account created successfully ✅ Your username is {username}. Please login."
        )

        return redirect("login")

    return render(request, "registartion.html")


# -------------------------
# Login
# Username OR Name OR Email + Password
# -------------------------

def login_view(request):

    if request.user.is_authenticated:
        return redirect("homePage")

    if request.method == "POST":

        login_value = request.POST.get("login", "").strip()
        password = request.POST.get("password", "")

        if not login_value or not password:
            messages.error(
                request,
                "Please enter username/email and password."
            )
            return redirect("login")

        user = None

        # Username Login
        user = authenticate(
            request,
            username=login_value,
            password=password
        )

        # Email Login
        if user is None:

            email_user = User.objects.filter(
                email__iexact=login_value
            ).first()

            if email_user:
                user = authenticate(
                    request,
                    username=email_user.username,
                    password=password
                )

        # Account Name Login
        if user is None:

            account = Account.objects.filter(
                name__iexact=login_value
            ).first()

            if account:

                account_user = User.objects.filter(
                    email__iexact=account.email
                ).first()

                if account_user:
                    user = authenticate(
                        request,
                        username=account_user.username,
                        password=password
                    )

        # Successful Login
        if user is not None:

            login(request, user)

            display_name = (
                user.first_name
                or user.username
                or user.email
            )

            messages.success(
                request,
                f"Welcome back, {display_name} 👋"
            )

            return redirect("homePage")

        messages.error(
            request,
            "Invalid username/email or password."
        )

        return redirect("login")

    return render(request, "login.html")


# -------------------------
# Logout
# -------------------------
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------------
# Home Page
# -------------------------
def homePage(request):

    if not request.user.is_authenticated:
        return redirect("login")

    return render(
        request,
        "index.html",
        {
            "email": request.user.email,
            "name": request.user.first_name,
            "username": request.user.username,
        }
    )

# -------------------------
# Static Pages
# -------------------------
@login_required(login_url="/login/")
def notes(request):
    return render(request, "notes.html")


@login_required(login_url="/login/")
def pomodoro(request):
    return render(request, "pomodoro.html")


@login_required(login_url="/login/")
def motivationbook(request):
    return render(request, "motivationbook.html")


# -------------------------
# User Dashboard
# -------------------------
@login_required(login_url="/login/")
def dashbored(request):
    user = request.user

    activities = UserActivity.objects.filter(user=user)

    today = timezone.localdate()

    today_activities = activities.filter(
        created_at__date=today
    )

    week_start = today - timedelta(days=6)

    week_activities = activities.filter(
        created_at__date__gte=week_start,
        created_at__date__lte=today
    )

    total_study_seconds = activities.filter(
        activity_type="study_stop"
    ).aggregate(
        total=Sum("duration_seconds")
    )["total"] or 0

    today_study_seconds = today_activities.filter(
        activity_type="study_stop"
    ).aggregate(
        total=Sum("duration_seconds")
    )["total"] or 0

    week_study_seconds = week_activities.filter(
        activity_type="study_stop"
    ).aggregate(
        total=Sum("duration_seconds")
    )["total"] or 0

    recent_activities = activities[:20]

    daily_data = []

    for i in range(6, -1, -1):
        current_day = today - timedelta(days=i)

        seconds = activities.filter(
            activity_type="study_stop",
            created_at__date=current_day
        ).aggregate(
            total=Sum("duration_seconds")
        )["total"] or 0

        daily_data.append({
            "date": current_day.strftime("%d %b"),
            "day": current_day.strftime("%a"),
            "seconds": seconds,
            "hours": round(seconds / 3600, 2)
        })

    context = {
        "user": user,
        "total_study_seconds": total_study_seconds,
        "today_study_seconds": today_study_seconds,
        "week_study_seconds": week_study_seconds,
        "recent_activities": recent_activities,
        "daily_data": daily_data,
    }

    return render(
        request,
        "userdashbored.html",
        context
    )


@login_required(login_url="/login/")
def record_activity(request):

    if request.method != "POST":
        return JsonResponse(
            {"success": False},
            status=405
        )

    activity_type = request.POST.get(
        "activity_type",
        "other"
    )

    title = request.POST.get(
        "title",
        "Activity"
    )

    description = request.POST.get(
        "description",
        ""
    )

    subject = request.POST.get(
        "subject",
        ""
    )

    try:
        duration_seconds = int(
            request.POST.get(
                "duration_seconds",
                0
            )
        )
    except (TypeError, ValueError):
        duration_seconds = 0

    UserActivity.objects.create(
        user=request.user,
        activity_type=activity_type,
        title=title[:255],
        description=description,
        subject=subject[:100],
        duration_seconds=max(
            duration_seconds,
            0
        )
    )

    return JsonResponse({
        "success": True
    })


# -------------------------
# To-Do
# -------------------------
@login_required(login_url="/login/")
def todo(request):

    tasks = Task.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "todo.html",
        {
            "tasks": tasks
        }
    )


@login_required(login_url="/login/")
def add_task(request):

    if request.method == "POST":

        text = request.POST.get("text", "").strip()

        if text:

            task = Task.objects.create(
                user=request.user,
                text=text
            )

            return JsonResponse(
                {
                    "id": task.id,
                    "text": task.text,
                    "completed": task.completed
                }
            )

    return JsonResponse(
        {
            "error": "Invalid request"
        },
        status=400
    )


@login_required(login_url="/login/")
def toggle_task(request, task_id):

    if request.method == "POST":

        task = get_object_or_404(
            Task,
            id=task_id,
            user=request.user
        )

        task.completed = not task.completed
        task.save()

        return JsonResponse(
            {
                "id": task.id,
                "completed": task.completed
            }
        )

    return JsonResponse(
        {
            "error": "POST required"
        },
        status=400
    )


@login_required(login_url="/login/")
def delete_task(request, task_id):

    if request.method == "POST":

        task = get_object_or_404(
            Task,
            id=task_id,
            user=request.user
        )

        task.delete()

        return JsonResponse(
            {
                "deleted": True
            }
        )

    return JsonResponse(
        {
            "error": "POST required"
        },
        status=400
    )


# -------------------------
# Journal
# -------------------------
@login_required(login_url="/login/")
def journal_page(request):

    entries = JournalEntry.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "journal.html",
        {
            "journal_entries": entries
        }
    )


@login_required(login_url="/login/")
def save_journal(request):

    if request.method == "POST":

        content = request.POST.get("content", "").strip()

        if content:

            entry = JournalEntry.objects.create(
                user=request.user,
                content=content
            )

            return JsonResponse(
                {
                    "id": entry.id,
                    "content": entry.content
                }
            )

    return JsonResponse(
        {
            "error": "Invalid request"
        },
        status=400
    )


@login_required(login_url="/login/")
def delete_journal(request, entry_id):

    if request.method == "POST":

        entry = get_object_or_404(
            JournalEntry,
            id=entry_id,
            user=request.user
        )

        entry.delete()

        return JsonResponse(
            {
                "deleted": True
            }
        )

    return JsonResponse(
        {
            "error": "POST required"
        },
        status=400
    )


# -------------------------
# Timetable
# -------------------------
@login_required(login_url="/login/")
def timetable(request):

    tasks = TimetableTask.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "timetable.html",
        {
            "tasks": tasks
        }
    )


@login_required(login_url="/login/")
def timetable_add_task(request):

    if request.method == "POST":

        text = request.POST.get("text", "").strip()

        if text:

            task = TimetableTask.objects.create(
                user=request.user,
                text=text
            )

            return JsonResponse(
                {
                    "id": task.id,
                    "text": task.text
                }
            )

    return JsonResponse(
        {
            "error": "Invalid request"
        },
        status=400
    )


@login_required(login_url="/login/")
def timetable_toggle_task(request, task_id):

    if request.method == "POST":

        task = get_object_or_404(
            TimetableTask,
            id=task_id,
            user=request.user
        )

        task.completed = not task.completed
        task.save()

        return JsonResponse(
            {
                "completed": task.completed
            }
        )

    return JsonResponse(
        {
            "error": "POST required"
        },
        status=400
    )


@login_required(login_url="/login/")
def timetable_delete_task(request, task_id):

    if request.method == "POST":

        task = get_object_or_404(
            TimetableTask,
            id=task_id,
            user=request.user
        )

        task.delete()

        return JsonResponse(
            {
                "deleted": True
            }
        )

    return JsonResponse(
        {
            "error": "POST required"
        },
        status=400
    )

