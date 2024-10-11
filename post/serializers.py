from django.contrib.auth.models import User
from rest_framework import serializers
from post.models import Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        post = Post.objects.create(user=user, **validated_data)
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance
