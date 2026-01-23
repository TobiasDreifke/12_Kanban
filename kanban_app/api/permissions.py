"""Custom permission classes for kanban_app API.

Contains permission checks used by API views to ensure that only board
owners or members can access or modify boards, tasks and comments.
"""

from ..models import Task
from django.shortcuts import get_object_or_404
from rest_framework import permissions


class IsBoardMemberOrOwner(permissions.BasePermission):
    """Allow owners and board members to access or modify a board."""
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.owner == request.user

        return (
            obj.owner == request.user
            or obj.members.filter(id=request.user.id).exists()
        )


class IsMemberOfTaskBoard(permissions.BasePermission):
    """Ensure the requesting user is a member or owner of a task's board."""
    def has_permission(self, request, view):
        task_id = view.kwargs.get('task_id')

        if task_id:
            task = get_object_or_404(Task, id=task_id)
            board = task.board
            return (
                board.owner == request.user
                or board.members.filter(id=request.user.id).exists()
            )

        return True

    def has_object_permission(self, request, view, obj):
        """Return True when the request user is the board owner or a member."""
        board = obj.board
        user = request.user
        return board.owner == user or board.members.filter(id=user.id).exists()


class IsAuthor(permissions.BasePermission):
    """Allow access only when the request user is the object's author."""
    def has_object_permission(self, request, view, obj):
        """Check that the current user authored the object."""
        return obj.author == request.user
