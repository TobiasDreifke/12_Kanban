from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, related_name='boards')

    def __str__(self):
        return self.title


class Task(models.Model):
    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('done', 'Done')
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
