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

        # Update Friend count for LOGGED IN user
        total_friends = Friendship.objects.filter(profile = user, request=True, accept=True).count()
        user.friend_count = total_friends
        user.save() 

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
                
                # Update for LOGGED IN user
                relationship = Friendship.objects.filter(profile=profile, friend=friend).update(
                    request = friend_request,
                    accept = friend_accept
                )

                # Update for FRIEND
                f_relationship = Friendship.objects.filter(profile=friend, friend=profile).update(
                    request = friend_request,
                    accept = friend_accept
                )

                return Response({"message": "Friendship relationship updated successfully!"})
                
        except:
            # If theres no established relationship, create a new one

            # For LOGGED IN user
            relationship =  Friendship(
                profile=profile,
                friend=friend,
                request=friend_request,
                accept=friend_accept
            )
            relationship.save()

            # Create for FRIEND also
            relationship =  Friendship(
                profile=friend,
                friend=profile,
                request=friend_accept, # SWAP FOR WHEN FRIEND INSTANCE >>> REQUEST = FALSE, ACCEPT= TRUE
                accept=friend_request # REQUEST BECOMES ACCEPT AND ACCEPT BECOMES REQUEST
            )
            relationship.save()

            return Response({"message": "New Friendship relationship created successfully!"})
            

@api_view(["DELETE"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def DeleteFriendship(request):

    # This view deletes friendship relationships

    serializer = FriendshipSerializer(data = request.data)

    if serializer.is_valid(raise_exception=True):
        profile = request.user
        friend = serializer.validated_data["friend"]

        try:
            # Delete for LOGGED IN user
            Friendship.objects.filter(profile=profile, friend=friend).delete()

            # Delete for FRIEND
            Friendship.objects.filter(profile=friend, friend=profile).delete()

            return Response({
                "message": "{} and {} Friendship relatonship deleted successfully!".format(profile, friend)
            })

        except:
            return Response({
                "message": "Friendship relationship could not be found"
            })