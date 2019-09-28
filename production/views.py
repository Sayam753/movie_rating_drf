from production.serializers import UserSerializer
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from production.models import User, ProfileOfProduction, ProfileOfActor, ProfileOfDirector, ProfileOfUser
from production.serializers import ProfileOfProductionSerializer, ProfileOfActorSerializer, ProfileOfDirectorSerializer, ProfileOfUserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class UserCreate(CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer
    name = "account-create"


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    name = "view-profile"

    def get(self, request, format=None):
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({'error': 'User with such id does not exist.'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if user.grp == 'a':
            profile = user.profileofproduction
            serializer = ProfileOfProductionSerializer(profile)
        elif user.grp == 'b':
            profile = user.profileofactor
            serializer = ProfileOfActorSerializer(profile)
        elif user.grp == 'c':
            profile = user.profileofdirector
            serializer = ProfileOfDirectorSerializer(profile)
        else:
            profile = user.profileofuser
            serializer = ProfileOfUserSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
