from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from production.models import ProfileOfActor, ProfileOfDirector, ProfileOfUser
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class NewMovie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='')
    release_date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    directors = models.ManyToManyField(ProfileOfDirector, related_name='movies')
    actors = models.ManyToManyField(ProfileOfActor, related_name='movies')

    def __str__(self):
        return self.title

    @property
    def get_avg_rating(self):
        total_sum = 0.0
        n = 0
        for i in self.rate_set.all():
            n += 1
            total_sum += i.rating
        if n == 0:
            return '0'
        else:
            return f'{total_sum/n}'


class Rate(models.Model):
    m = models.ForeignKey(NewMovie, on_delete=models.CASCADE)
    u = models.ForeignKey(ProfileOfUser, on_delete=models.CASCADE)
    rating = models.FloatField(null=True, blank=True, default=0,
                               validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    rated_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.m} {self.u} {self.rating}'
