"""API views for the Kanban app.

This module exposes REST API endpoints for listing and managing
boards, tasks and comments. Views use Django REST Framework generic
views and custom permission classes located in `kanban_app.api.permissions`.
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import (
    BoardUpdateSerializer,
    CommentSerializer,
    TaskCreateSerializer,
    TaskListSerializer,
    TaskUpdateSerializer,
)
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Board, Task, Comment
from .permissions import IsAuthor, IsBoardMemberOrOwner, IsMemberOfTaskBoard
from .serializers import (
    BoardSerializer,
    BoardDetailSerializer,
    UserDetailSerializer,
)


class BoardListCreateView(generics.ListCreateAPIView):
    """List boards for the user and allow creating new boards."""
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return boards where the current user is owner or member."""
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        """Set the board owner to the requesting user on create."""
        serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a single board with permissions."""
    queryset = Board.objects.all()
    permission_classes = [IsBoardMemberOrOwner]

    def get_serializer_class(self):
        """Return the appropriate serializer for read vs update requests."""
        if self.request.method in ['PUT', 'PATCH']:
            return BoardUpdateSerializer
        return BoardDetailSerializer


class EmailCheckView(APIView):
    """Endpoint to check whether an email corresponds to a user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return user details if the provided email exists."""
        email = request.query_params.get('email')

        if not email:
            return Response(
                {"error": "Email parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"detail": "Email not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class AssignedTaskView(generics.ListAPIView):
    """List tasks assigned to the current user."""
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tasks where the requesting user is the assignee."""
        user = self.request.user
        return Task.objects.filter(assignee=user).distinct()


class ReviewerTaskView(generics.ListAPIView):
    """List tasks where the current user is the reviewer."""
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return tasks where the requesting user is the reviewer."""
        user = self.request.user
        return Task.objects.filter(reviewer=user).distinct()


class TaskCreateView(generics.CreateAPIView):
    """Create a new task on a board if the user is a member or owner."""
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Validate membership then save the new task with provided data."""
        board = serializer.validated_data.get('board')
        user = self.request.user

        is_member = board.members.filter(id=user.id).exists()
        is_owner = (board.owner == user)

        if not (is_member or is_owner):
            raise PermissionDenied(
                "You must be a member or owner of the board to create tasks.")

        serializer.save()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a task with board membership checks."""
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsMemberOfTaskBoard]

    def get_serializer_class(self):
        """Return update serializer for modifying tasks, create for reads."""
        if self.request.method in ['PUT', 'PATCH']:
            return TaskUpdateSerializer
        return TaskCreateSerializer

    def perform_update(self, serializer):
        """Prevent changing the task's board during update, then save."""
        if 'board' in serializer.validated_data:
            serializer.validated_data.pop('board')
        serializer.save()


class CommentView(generics.ListCreateAPIView):
    """List and create comments for a specific task."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsMemberOfTaskBoard]

    def get_queryset(self):
        """Return comments belonging to the task identified by URL kwarg."""
        task_id = self.kwargs.get('task_id')
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        """Attach the requesting user as author and link the comment to task."""
        task_id = self.kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        serializer.save(author=self.request.user, task=task)


class CommentDetailView(generics.RetrieveDestroyAPIView):
    """Retrieve or delete a specific comment on a task (author-only)."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    lookup_url_kwarg = 'comment_id'

    def get_object(self):
        """Retrieve the comment matching both task and comment URL params."""
        task_id = self.kwargs.get('task_id')
        comment_id = self.kwargs.get('comment_id')
        obj = get_object_or_404(Comment, id=comment_id, task_id=task_id)
        self.check_object_permissions(self.request, obj)
        return obj
