from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Post, Comment, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment
        read_only_fields = ['post']


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username",
                                        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")

    class Meta:
        fields = ['user', 'following']
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate_following(self, following):
        """Валидатор запрета подписки на самого себя"""

        if self.context['request'].user == following:
            raise serializers.ValidationError(
                'На себя подписаться нельзя')
        return following
