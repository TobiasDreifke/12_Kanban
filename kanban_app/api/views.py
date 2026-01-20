from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import CommentSerializer, TaskSerializer
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
    TaskSerializer,
    UserDetailSerializer,
)


class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [IsBoardMemberOrOwner]


class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user).distinct()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class ReviewerTaskView(generics.ListAPIView):
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer=user).distinct()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        board = serializer.validated_data.get('board')
        user = self.request.user

        is_member = board.members.filter(id=user.id).exists()
        is_owner = (board.owner == user)

        if not (is_member or is_owner):
            raise PermissionDenied(
                "You must be a member or owner of the board to create tasks.")

        serializer.save()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsMemberOfTaskBoard]

    def perform_update(self, serializer):
        if 'board' in serializer.validated_data:
            serializer.validated_data.pop('board')
        serializer.save()


class CommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsMemberOfTaskBoard]

    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        serializer.save(author=self.request.user, task=task)


class CommentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    lookup_url_kwarg = 'comment_id'

    def get_object(self):
        task_id = self.kwargs.get('task_id')
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comment, id=comment_id, task_id=task_id)
