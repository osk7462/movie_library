from rest_framework import serializers
from .models import Movie, Collection
from django.contrib.auth.admin import User
from django.core.exceptions import ObjectDoesNotExist


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid']


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)
    top_genre = serializers.CharField(required=False)

    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description',
                  'movies', 'user', 'top_genre']
        depth = 1
        read_only_fields = ['uuid', 'user', 'top_genre']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.action = kwargs.pop('action', None)
        super().__init__(*args, **kwargs)


    def create(self, validated_data):
        movies = validated_data.pop('movies')
        collection = Collection.objects.create(
            **validated_data, user=self.user)
        for movie in movies:
            movie_object, created = Movie.objects.get_or_create(**movie)
            collection.movies.add(movie_object)
        return collection

    #this validator checks for duplication of a collection for a user
    def validate_title(self, value): 
        if self.action == 'create':
            if Collection.objects.filter(title=value, user=self.user).exists():
                raise serializers.ValidationError("collection already exist")
        return value

    def update(self, instance, validated_data):
        movies = validated_data.pop('movies')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        for movie in movies:
            try:    #this block checks for movie duplication in a collection
                movie_object = (instance.movies).get(uuid=movie.get('uuid'))
                movie_object.title = movie.get('title', movie_object.title)
                movie_object.description = movie.get(
                    'descriptiom', movie_object.description)
                movie_object.genres = movie.get('genres', movie_object.genres)
                movie_object.save()
            except ObjectDoesNotExist:
                new_movie_object, created = Movie.objects.get_or_create(**movie)
                instance.movies.add(new_movie_object)

        instance.save()
        return instance
