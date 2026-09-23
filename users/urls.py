from django.urls import path
from . import views


urlpatterns = [
    path("registartion/", views.registartion, name="registartion"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.homePage, name="homePage"),

    path("notes/", views.notes, name="notes"),
    path("pomodoro/", views.pomodoro, name="pomodoro"),
    path("motivationbook/", views.motivationbook, name="motivationbook"),
    path("dashbored/", views.dashbored, name="dashbored"),
    path(
    "activity/record/",
    views.record_activity,
    name="record_activity"
),
   

    path("todo/", views.todo, name="todo"),
    path("todo/add/", views.add_task, name="add_task"),
    path("todo/toggle/<int:task_id>/", views.toggle_task, name="toggle_task"),
    path("todo/delete/<int:task_id>/", views.delete_task, name="delete_task"),

    path("journal/", views.journal_page, name="journal"),
    path("journal/save/", views.save_journal, name="save_journal"),
    path("journal/delete/<int:entry_id>/", views.delete_journal, name="delete_journal"),

    path("timetable/", views.timetable, name="timetable"),
    path("timetable/add/", views.timetable_add_task, name="timetable_add_task"),
    path("timetable/toggle/<int:task_id>/", views.timetable_toggle_task, name="timetable_toggle_task"),
    path("timetable/delete/<int:task_id>/", views.timetable_delete_task, name="timetable_delete_task"),
]
