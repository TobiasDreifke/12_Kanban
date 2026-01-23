"""Serializers for kanban_app API.

Convert model instances (Board, Task, Comment) and User data to and
from JSON representations used by the REST API. Includes create/update
validation rules specific to the domain (e.g., board membership checks).
"""

from rest_framework import serializers
from ..models import Board, Task, Comment
from django.contrib.auth.models import User


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for Board model with summary fields."""
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'member_count', 'ticket_count',
            'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id', 'members'
        ]

    def get_member_count(self, obj):
        """Return the number of members on the board."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Return the number of tasks associated with the board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Return count of tasks with status 'to-do' on the board."""
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        """Return count of high priority tasks on the board."""
        return obj.tasks.filter(priority='high').count()


class UserDetailSerializer(serializers.ModelSerializer):
    """Compact user representation used in nested serializer fields."""
    fullname = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class TaskListSerializer(serializers.ModelSerializer):
    """Lightweight task serializer for list endpoints."""
    board = serializers.PrimaryKeyRelatedField(read_only=True)
    assignee = UserDetailSerializer(read_only=True)
    reviewer = UserDetailSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'due_date', 'comments_count'
        ]

    def get_comments_count(self, obj):
        """Return number of comments attached to the task."""
        return obj.comments.count()


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer used to create tasks, validates board membership."""

    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        write_only=True,
        required=False,
        allow_null=True
    )

    assignee = UserDetailSerializer(read_only=True)

    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        write_only=True,
        required=False,
        allow_null=True
    )

    reviewer = UserDetailSerializer(read_only=True)

    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'due_date', 'comments_count',
            'board_id', 'reviewer_id', 'assignee_id',
        ]

    def validate(self, data):
        """Validate assignee and reviewer are members or owner of the board."""
        board = data.get('board')

        if board is None and self.instance:
            board = self.instance.board

        assignee = data.get('assignee')
        reviewer = data.get('reviewer')

        if assignee:
            is_member = board.members.filter(id=assignee.id).exists()
            is_owner = (board.owner == assignee)
            if not (is_member or is_owner):
                raise serializers.ValidationError(
                    {"assignee_id": "User is not a member of this board."})

        if reviewer:
            is_member = board.members.filter(id=reviewer.id).exists()
            is_owner = (board.owner == reviewer)
            if not (is_member or is_owner):
                raise serializers.ValidationError(
                    {"reviewer_id": "User is not a member of this board."})

        return data

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating tasks with assignee/reviewer helpers."""
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        write_only=True,
        required=False,
        allow_null=True
    )

    assignee = UserDetailSerializer(read_only=True)

    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        write_only=True,
        required=False,
        allow_null=True
    )

    reviewer = UserDetailSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'due_date',
            'reviewer_id', 'assignee_id',
        ]

    def validate(self, data):
        """Validate updates ensure assignee/reviewer belong to the task's board."""
        board = self.instance.board

        assignee = data.get('assignee')
        reviewer = data.get('reviewer')

        if assignee:
            is_member = board.members.filter(id=assignee.id).exists()
            is_owner = (board.owner == assignee)
            if not (is_member or is_owner):
                raise serializers.ValidationError(
                    {"assignee_id": "User is not a member of this board."})

        if reviewer:
            is_member = board.members.filter(id=reviewer.id).exists()
            is_owner = (board.owner == reviewer)
            if not (is_member or is_owner):
                raise serializers.ValidationError(
                    {"reviewer_id": "User is not a member of this board."})

        return data


class BoardDetailSerializer(serializers.ModelSerializer):
    """Detailed board serializer including members and tasks."""
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = UserDetailSerializer(many=True, read_only=True)
    tasks = TaskListSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class BoardUpdateSerializer(serializers.ModelSerializer):
    """Serializer used to update board membership and title."""
    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True
    )
    owner_data = UserDetailSerializer(source='owner', read_only=True)
    members_data = UserDetailSerializer(
        source='members', many=True, read_only=True)
    tasks = TaskListSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data',
                  'members', 'members_data', 'tasks']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments displayed in task contexts."""
    author = serializers.ReadOnlyField(source='author.first_name')

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
