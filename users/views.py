# users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# If you still have a separate Account model as profile, keep import but optional:
from .models import Account, Task, JournalEntry, TimetableTask


# -------------------------
# Registration / Login / Logout (using Django's User)
# -------------------------
def registartion(request):
    # if already logged in, send to home
    if request.user.is_authenticated:
        return redirect("homePage")

    if request.method == "POST":
        name = request.POST.get("name") or ""
        email = request.POST.get("email") or ""
        mobile = request.POST.get("mobile") or ""
        password = request.POST.get("password") or ""
        username = email.strip().lower()  # use email as username (unique)

        if not email or not password:
            messages.error(request, "Please provide email and password.")
            return redirect("registartion")

        # If user already exists -> try to authenticate (login)
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Welcome back ✅")
                return redirect("homePage")
            else:
                messages.error(request, "Account exists but wrong password.")
                return redirect("registartion")

        # Create new Django User
        user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
        user.save()

        # Optional: keep your old Account model as profile (if you need it)
        try:
            # if Account model has fields name,email,mobile,password
            # adjust depending on your Account model signature
            if not Account.objects.filter(email=email).exists():
                Account.objects.create(name=name, email=email, mobile=mobile, password=password)
        except Exception:
            # ignore if Account model is different
            pass

        login(request, user)
        messages.success(request, "Account created and logged in ✅")
        return redirect("homePage")

    return render(request, "registartion.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully ✅")
    return redirect("registartion")


def homePage(request):
    if request.user.is_authenticated:
        return render(request, "index.html", {"email": request.user.email, "name": request.user.first_name})
    return redirect("registartion")


# -------------------------
# Static pages (require login)
# -------------------------
@login_required(login_url="/registartion/")
def notes(request):
    return render(request, "notes.html")


@login_required(login_url="/registartion/")
def pomodoro(request):
    return render(request, "pomodoro.html")


@login_required(login_url="/registartion/")
def motivationbook(request):
    return render(request, "motivationbook.html")

@login_required(login_url="/registartion/")
def dashbored(request):
    return render(
        request,
        "userdashbored.html",
        {
            "user_name": request.user.first_name,  # jo registration me name diya tha
            "user_email": request.user.email,      # email
        },
    )


# -------------------------
# To-Do (expects Task.user -> Django User)
# -------------------------
@login_required(login_url="/registartion/")
def todo(request):
    tasks = Task.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "todo.html", {"tasks": tasks})


@login_required(login_url="/registartion/")
def add_task(request):
    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            task = Task.objects.create(user=request.user, text=text)
            return JsonResponse({"id": task.id, "text": task.text, "completed": task.completed})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required(login_url="/registartion/")
def toggle_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.completed = not task.completed
        task.save()
        return JsonResponse({"id": task.id, "completed": task.completed})
    return JsonResponse({"error": "POST required"}, status=400)


@login_required(login_url="/registartion/")
def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
        return JsonResponse({"deleted": True})
    return JsonResponse({"error": "POST required"}, status=400)


# -------------------------
# Journal
# -------------------------
@login_required(login_url="/registartion/")
def journal_page(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "journal.html", {"journal_entries": entries})


@login_required(login_url="/registartion/")
def save_journal(request):
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            entry = JournalEntry.objects.create(user=request.user, content=content)
            return JsonResponse({"id": entry.id, "content": entry.content})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required(login_url="/registartion/")
def delete_journal(request, entry_id):
    if request.method == "POST":
        entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
        entry.delete()
        return JsonResponse({"deleted": True})
    return JsonResponse({"error": "POST required"}, status=400)


# -------------------------
# Timetable
# -------------------------
@login_required(login_url="/registartion/")
def timetable(request):
    tasks = TimetableTask.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "timetable.html", {"tasks": tasks})


@login_required(login_url="/registartion/")
def timetable_add_task(request):
    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            task = TimetableTask.objects.create(user=request.user, text=text)
            return JsonResponse({"id": task.id, "text": task.text})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required(login_url="/registartion/")
def timetable_toggle_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(TimetableTask, id=task_id, user=request.user)
        task.completed = not task.completed
        task.save()
        return JsonResponse({"completed": task.completed})
    return JsonResponse({"error": "POST required"}, status=400)


@login_required(login_url="/registartion/")
def timetable_delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(TimetableTask, id=task_id, user=request.user)
        task.delete()
        return JsonResponse({"deleted": True})
    return JsonResponse({"error": "POST required"}, status=400)
