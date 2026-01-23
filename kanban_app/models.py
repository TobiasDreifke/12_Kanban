"""Models for the Kanban app.

This module defines the data models used by the kanban_app: Board, Task
and Comment. These represent boards, tasks/tickets and threaded comments
attached to tasks. Models reference Django's built-in `User` model.
"""

from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    """A kanban board with an owner and members."""
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, related_name='boards')

    def __str__(self):
        return self.title


class Task(models.Model):
    """A task/ticket that belongs to a board with status and priority."""
    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('done', 'Done'),
        ('review', 'Review')
    ]
    PRIO_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='to-do')
    priority = models.CharField(
        max_length=20, choices=PRIO_CHOICES, default='medium')

    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='reviewed_tasks')

    due_date = models.DateField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    """A comment left by a user on a task."""
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"
