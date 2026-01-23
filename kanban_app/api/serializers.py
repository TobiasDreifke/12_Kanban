from rest_framework import serializers
from ..models import Board, Task, Comment
from django.contrib.auth.models import User


class BoardSerializer(serializers.ModelSerializer):
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
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()


class UserDetailSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']


class TaskListSerializer(serializers.ModelSerializer):
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
        return obj.comments.count()


class TaskCreateSerializer(serializers.ModelSerializer):
    # board_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Board.objects.all(),
    #     source='board',
    #     write_only=True,
    #     required=True,  
    #     allow_null=False, 
    #     error_messages={
    #         'does_not_exist': 'Board with id {pk_value} does not exist.',
    #         'required': 'This field is required.'
    #     }
    # )

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
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = UserDetailSerializer(many=True, read_only=True)
    tasks = TaskListSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


class BoardUpdateSerializer(serializers.ModelSerializer):
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
    author = serializers.ReadOnlyField(source='author.first_name')

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
