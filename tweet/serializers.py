from rest_framework import serializers
from .models import User, Tweet

class UserSerializer(serializers.HyperlinkedModelSerializer):
    tweets = serializers.HyperlinkedRelatedField(many=True, view_name='tweet-detail', read_only=True)
    follower_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'is_following', 'follower_count',
                    'following_count', 'tweets', 'email', 'password']
        extra_kwargs = {
            'password':{'write_only':True, 'required':True},
            'email':{'write_only':True, 'required':True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def get_is_following(self, obj):
        try:
            logged_in_user = self.context['request'].user
            is_following = logged_in_user.following.filter(id=obj.id).exists()
            return is_following
        except AttributeError:
            # always False for non-authenticated user
            return False

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