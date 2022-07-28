from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from .serializers import FriendshipSerializer
from .models import Friendship
from rest_framework import generics
from backend.models import User

# Create your views here.

class ListFriendsAPIView(generics.ListAPIView):
    # This view returns friend relationships of currently logged in user

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user = self.request.user

        return Friendship.objects.filter(profile = user)


@api_view(["PUT"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def UpdateFriendship(request):

    # This View helps with creating friendships relationships
    # Friendship relationship would be created if none exsits
    # Friendship updates take place if relationship exsits

    serializer = FriendshipSerializer(data = request.data)

    if serializer.is_valid(raise_exception=True):
        profile = request.user
        friend = serializer.validated_data["friend"] # FRIEND ID
        friend_request = serializer.validated_data["request"]
        friend_accept = serializer.validated_data["accept"]

        try:
            # Check if there's already an established relationship to updated
            registered_relationship = Friendship.objects.get(profile=profile, friend=friend)
            if registered_relationship:

                relationship = Friendship.objects.filter(profile=profile, friend=friend).update(
                    request = friend_request,
                    accept = friend_accept
                )

                # Update friend count of current user where request and accept are True
                total_friends = Friendship.objects.filter(profile = profile, request=True, accept=True).count()
                profile.friend_count = total_friends
                profile.save()

                return Response({"message": "Friendship relationship updated successfully!"})

        except:
            # If theres no established relationship, create a new one
            relationship =  Friendship(
                profile=profile,
                friend=friend,
                request=friend_request,
                accept=friend_accept
            )
            relationship.save()

            # Update friend count of current user where request and accept are True
            total_friends = Friendship.objects.filter(profile = profile, request=True, accept=True).count()
            profile.friend_count = total_friends
            profile.save()

            return Response({"message": "New Friendship relationship created successfully!"})
