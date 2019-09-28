from rest_framework import serializers
from movie.models import NewMovie, Rate
from production.serializers import ProfileOfActorSerializer, ProfileOfDirectorSerializer


class NewMovieSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    actors = ProfileOfActorSerializer(read_only=True, many=True)
    directors = ProfileOfDirectorSerializer(read_only=True, many=True)

    class Meta:
        model = NewMovie
        fields = ('id', 'title', 'description', 'release_date', 'author', 'actors', 'directors',)


class RateSerializer(serializers.ModelSerializer):
    m = serializers.ReadOnlyField(source='m.title')
    u = serializers.ReadOnlyField(source='u.user.email')

    class Meta:
        model = Rate
        fields = ('id', 'm', 'u', 'rating', 'rated_on')
