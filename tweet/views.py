from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from .models import User, Tweet
from .serializers import TweetSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly, IsUserOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrReadOnly]

    @action(detail=True, permission_classes=[permissions.IsAuthenticated], methods=['post'])
    def follow_unfollow(self, request, *args, **kwargs):
        view_user = self.get_object()
        auth_user = request.user
        if view_user == auth_user:
            return Response({'response': 'You cannot follow yourself'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            if auth_user.following.filter(id=view_user.id).exists():
                # unfollow
                auth_user.following.remove(view_user)
            else:
                # follow
                auth_user.following.add(view_user)

            serializer = UserSerializer(view_user, context={'request': request})
            return Response(serializer.data)

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, permission_classes=[permissions.IsAuthenticated], methods=['post'])
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