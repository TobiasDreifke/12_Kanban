
from django.urls import path

from kanban_app.api.views import CommentView, CommentDetailView, TaskDetailView, BoardListCreateView, BoardDetailView, EmailCheckView, AssignedTaskView, ReviewerTaskView, TaskCreateView

urlpatterns = [
    path('api/boards/', BoardListCreateView.as_view(), name='board-list'),
    path('api/boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('api/email-check/', EmailCheckView.as_view(), name='login'),

    path('api/tasks/assigned-to-me/', AssignedTaskView.as_view(), name='assigned-tasks'),
    path('api/tasks/reviewing/', ReviewerTaskView.as_view(), name='reviewing-tasks'),
    path('api/tasks/', TaskCreateView.as_view(), name='add-task'),

    path('api/tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    path('api/tasks/<int:task_id>/comments/',
         CommentView.as_view(), name='task-comments'),
    path('api/tasks/<int:task_id>/comments/<int:comment_id>/',
         CommentDetailView.as_view(), name='comment-detail'),
]
