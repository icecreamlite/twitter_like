from rest_framework import serializers
from .models import User, Tweet

class UserSerializer(serializers.HyperlinkedModelSerializer):
    tweets = serializers.HyperlinkedRelatedField(many=True, view_name='tweet-detail', read_only=True)
    follower_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'follower_count', 'following_count', 'tweets']

class TweetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    like_count = serializers.IntegerField(source='like.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = ['url', 'id', 'owner', 'tweet_text', 'like_count', 'is_liked']

    def get_is_liked(self, obj):
        try:
            logged_in_user = self.context['request'].user
            is_liked = obj.like.filter(id=logged_in_user.id).exists()
            return is_liked
        except AttributeError:
            # always False for non-authenticated user
            return False