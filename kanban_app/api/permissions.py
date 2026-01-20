from rest_framework import permissions


class IsBoardMemberOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.owner == request.user

        return obj.owner == request.user or obj.members.filter(id=request.user.id).exists()

from rest_framework import permissions
from django.shortcuts import get_object_or_404
from ..models import Task

class IsMemberOfTaskBoard(permissions.BasePermission):
    def has_permission(self, request, view):
        task_id = view.kwargs.get('task_id')
        
        if task_id:
            task = get_object_or_404(Task, id=task_id)
            board = task.board
            return board.owner == request.user or board.members.filter(id=request.user.id).exists()
        
        return True

    def has_object_permission(self, request, view, obj):
        board = obj.board 
        user = request.user
        return board.owner == user or board.members.filter(id=user.id).exists()
    
class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user