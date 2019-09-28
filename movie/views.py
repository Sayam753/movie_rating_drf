from django.db import IntegrityError
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from .models import NewMovie, Rate
from .permissions import IsProduction, IsUser
from .serializers import NewMovieSerializer, RateSerializer
from production.models import User, ProfileOfUser, ProfileOfActor, ProfileOfDirector


# Create your views here.
class MovieListCreateView(APIView):
    permission_classes = (IsProduction, )
    throttle_classes = [UserRateThrottle]
    name = "movie-list-create"

    def get(self, request, format=None):
        movies = NewMovie.objects.all()
        serializer = NewMovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        try:
            # checking actors
            actors_list = list()
            if 'actors' in data:
                invalid_actors_list = list()
                for email in data['actors']:
                    try:
                        actor_user = User.objects.get(email=email)
                        actors_list.append(actor_user.profileofactor)
                    except User.DoesNotExist or User.profileofactor.RelatedObjectDoesNotExist:
                        invalid_actors_list.append(email)
                if len(invalid_actors_list) > 0:
                    return Response({'error': f'The following actors {invalid_actors_list} do not exist.'},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # checking directors
            directors_list = list()
            if 'directors' in data:
                invalid_directors_list = list()
                for email in data['directors']:
                    try:
                        director_user = User.objects.get(email=email)
                        directors_list.append(director_user.profileofdirector)
                    except User.DoesNotExist or User.profileofdirector.RelatedObjectDoesNotExist:
                        invalid_directors_list.append(email)
                if len(invalid_directors_list) > 0:
                    return Response({'error': f'The following directors {invalid_directors_list} do not exist.'},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            user = User.objects.get(email=request.user.email)
            movie = NewMovie.objects.create(title=data['title'], description=data['description'],
                                            release_date=data['release_date'], author=user)
            movie.actors.set(actors_list)
            movie.directors.set(directors_list)
            movie.save()
            data = NewMovieSerializer(movie).data
            return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Movie with such title already exists.'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class RateCreateView(APIView):
    permission_classes = (IsUser, )
    throttle_classes = [UserRateThrottle]
    name = "rate-create"

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        try:
            movie = NewMovie.objects.get(title=data['movie'])
        except NewMovie.DoesNotExist:
            return Response({'error': 'Movie with such title already exists.'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = User.objects.get(email=request.user.email)
        profile = ProfileOfUser.objects.get(user=user)
        for rate in profile.rate_set.all():
            if rate.m == movie:
                return Response({'error': 'User has already rated the movie.'},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        rate = Rate.objects.create(m=movie, u=profile, rating=data['rating'])
        rate.save()
        data = RateSerializer(rate).data
        return Response(data, status=status.HTTP_201_CREATED)

