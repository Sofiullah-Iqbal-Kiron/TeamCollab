from rest_framework import serializers

from ..models import User, Project, Task, Comment


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%d %B %Y, %I:%M %p", read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'date_joined'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_confirmation',
            'email',
            'first_name',
            'last_name'
        ]

    def validate(self, attrs):
        password1 = attrs['password']
        password2 = attrs['password_confirmation']

        if password1 != password2:
            raise serializers.ValidationError("Passwords didn't match!")

        return attrs

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']

        registered_user = User.objects.create_user(username, email, password)
        registered_user.first_name = validated_data.get('first_name', '')
        registered_user.last_name = validated_data.get('last_name', '')
        registered_user.save()

        return registered_user


class ProjectSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %B %Y, %I:%M %p")

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'owner',
            'created_at',

            # reverse fields
            'developers',
            'tasks'
        ]


class TaskSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %B %Y, %I:%M %p")
    due_date = serializers.DateTimeField(format="%d %B %Y, %I:%M %p")

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %B %Y, %I:%M %p")
    due_date = serializers.DateTimeField(format="%d %B %Y, %I:%M %p")

    class Meta:
        model = Task
        exclude = ['project']


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %B %Y, %I:%M %p")

    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %B %Y, %I:%M %p")
    
    class Meta:
        model = Comment
        exclude = ['task']