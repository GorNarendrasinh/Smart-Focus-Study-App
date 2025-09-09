from django.contrib import admin
from .models import Account, Task, JournalEntry,TimetableTask

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "mobile", "date")  # admin me columns show honge
   

# Task model ko admin me register karo
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'completed', 'created_at')
    list_filter = ('completed', 'created_at')
    search_fields = ('text', 'user__username')
    ordering = ('-created_at',)

# JournalEntry model ko admin me register karo
@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'created_at')
    search_fields = ('content', 'user__username')
    ordering = ('-created_at',)



@admin.register(TimetableTask)
class TimetableTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'completed', 'created_at')
    list_filter = ('completed', 'created_at', 'user')
    search_fields = ('text', 'user__username')
    ordering = ('-created_at',)    