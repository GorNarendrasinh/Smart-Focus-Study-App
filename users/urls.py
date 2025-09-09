from django.urls import path
from . import views

urlpatterns = [
    # Home + Auth
    path('', views.homePage, name='homePage'),
    path('registartion/', views.registartion, name='registartion'),
    path('logout/', views.logout_user, name='logout'),

    # Static Pages
    path('motivationbook/', views.motivationbook, name='motivationbook'),
    path('notes/', views.notes, name='notes'),
    path('pomodoro/', views.pomodoro, name='pomodoro'),
    path('userdashbored/', views.dashbored, name='userdashbored'),

    # To-Do
    path('todo/', views.todo, name='todo'),
    path('add-task/', views.add_task, name='add_task'),
    path('toggle-task/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),

    # Journal
    path('journal/', views.journal_page, name='journal_page'),
    path('save-journal/', views.save_journal, name='save_journal'),
    path('delete-journal/<int:entry_id>/', views.delete_journal, name='delete_journal'),

    # Timetable
    path('timetable/', views.timetable, name='timetable'),
    path('timetable/add/', views.timetable_add_task, name='timetable_add_task'),
    path('timetable/toggle/<int:task_id>/', views.timetable_toggle_task, name='timetable_toggle_task'),
    path('timetable/delete/<int:task_id>/', views.timetable_delete_task, name='timetable_delete_task'),
]
