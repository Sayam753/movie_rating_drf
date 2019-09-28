from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
CHOICES = (('a', 'is_production_company'), ('b', 'is_actor'), ('c', 'is_director'), ('d', 'public_user'),)


class User(AbstractUser):
    username = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    phone_no = models.CharField(max_length=12)
    birth_date = models.DateField()
    biography = models.CharField(max_length=100, default='')
    grp = models.CharField(choices=CHOICES, max_length=10)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_no', 'birth_date', 'biography', 'grp']

    def __str__(self):
        return "{}".format(self.email)


class ProfileOfProduction(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profileofproduction')

    def __str__(self):
        return f'{self.user}'


class ProfileOfActor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profileofactor')

    def max_rating(self):
        high = -1
        u = User.objects.get(email=self.user.email)
        for r in u.profileofactor.movies.all():
            d = float(r.get_avg_rating)
            if d > high:
                high = d
        if high == -1:
            return 'No rating given'
        else:
            return f'{high}'

    def min_rating(self):
        low = 100
        u = User.objects.get(email=self.user.email)
        for r in u.profileofactor.movies.all():
            d = float(r.get_avg_rating)
            if d < low:
                low = d
        if low == 100:
            return 'No rating given'
        else:
            return f'{low}'

    def __str__(self):
        return f'{self.user}'


class ProfileOfDirector(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profileofdirector')

    def max_rating(self):
        high = -1
        u = User.objects.get(email=self.user.email)
        for r in u.profileofdirector.movies.all():
            d = float(r.get_avg_rating)
            if d > high:
                high = d
        if high == -1:
            return 'No rating given'
        else:
            return f'{high}'

    def min_rating(self):
        low = 100
        u = User.objects.get(email=self.user.email)
        for r in u.profileofdirector.movies.all():
            d = float(r.get_avg_rating)
            if d < low:
                low = d
        if low == 100:
            return 'No rating given'
        else:
            return f'{low}'

    def __str__(self):
        return f'{self.user}'


class ProfileOfUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profileofuser')

    def get_avg_rating(self):
        n = 0
        total_sum = 0.0
        u = User.objects.get(email=self.user.email)
        for r in u.profileofuser.rate_set.all():
            total_sum += r.rating
            n += 1
        if n == 0:
            return f'No rating given'
        else:
            return f'{total_sum / n}'

    def max_rating(self):
        high = -1
        u = User.objects.get(email=self.user.email)
        for r in u.profileofuser.rate_set.all():
            if r.rating > high:
                high = r.rating
        if high == -1:
            return 'No rating given'
        else:
            return f'{high}'

    def min_rating(self):
        low = 100
        u = User.objects.get(email=self.user.email)
        for r in u.profileofuser.rate_set.all():
            if r.rating < low:
                low = r.rating
        if low == 100:
            return 'No rating given'
        else:
            return f'{low}'

    def __str__(self):
        return f'{self.user}'


