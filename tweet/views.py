from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from .models import User, Tweet
from .serializers import TweetSerializer, UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    def like_unlike(self, request, *args, **kwargs):
        tweet = self.get_object()
        user = request.user
        if tweet.like.filter(id=user.id).exists():
            # unlike
            tweet.like.remove(request.user)
        else:
            #like
            tweet.like.add(request.user)
        serializer = TweetSerializer(tweet, context={'request':request})
        return Response(serializer.data)

    # associate tweet to authenticated user
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)