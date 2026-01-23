"""URL routes for the kanban_app REST API.

Defines endpoints for boards, tasks and task comments. These routes are
included into the project's main URL configuration under the `api/` path.
"""

from django.urls import path

from kanban_app.api.views import CommentView, CommentDetailView, TaskDetailView, BoardListCreateView, BoardDetailView, EmailCheckView, AssignedTaskView, ReviewerTaskView, TaskCreateView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('email-check/', EmailCheckView.as_view(), name='login'),

    path('tasks/assigned-to-me/', AssignedTaskView.as_view(), name='assigned-tasks'),
    path('tasks/reviewing/', ReviewerTaskView.as_view(), name='reviewing-tasks'),
    path('tasks/', TaskCreateView.as_view(), name='add-task'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    path('tasks/<int:task_id>/comments/',
         CommentView.as_view(), name='task-comments'),
    path('tasks/<int:task_id>/comments/<int:comment_id>/',
         CommentDetailView.as_view(), name='comment-detail'),
]
