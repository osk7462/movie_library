from django.db import models
import uuid
from django.contrib.auth.admin import User
import operator


class Movie(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=10000, blank=True)
    genres = models.CharField(max_length=500, blank=True)
    uuid = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Collection(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=5000, blank=True)
    movies = models.ManyToManyField(Movie)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    #this method calculates top three genres for a user
    def top_genre(self):
        collections = Collection.objects.filter(user=self.user)
        genre_dict = {}
        for collection in collections:
            movies = collection.movies.all()
            for movie in movies:
                genres = movie.genres.split(",")
                for genre in genres:
                    count = genre_dict.get(genre, 0)
                    genre_dict[genre] = count + 1

        genre_dict.pop('', None)
        if genre_dict.keys():
            genre_dict = dict(
                sorted(genre_dict.items(), key=operator.itemgetter(1), reverse=True))
            genre_dict_list = list(genre_dict.keys())
            return ",".join(genre_dict_list[0:3]) if len(genre_dict_list) >= 3 else ",".join(genre_dict_list[0:len(genre_dict_list)])

        return " "
