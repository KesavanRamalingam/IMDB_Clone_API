from django.db import models, reset_queries
from django.db.models.base import ModelState
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils.translation import activate
from django.contrib.auth.models import User

class StreamPlatform(models.Model):
    name = models.CharField(max_length=256)
    about = models.CharField(max_length=256)
    website = models.URLField(max_length=256)

    def __str__(self):
        return self.name

class WatchList(models.Model):
    title = models.CharField(max_length=256)
    storyline = models.CharField(max_length=256)
    platform = models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name='watchlist')
    avg_ratings = models.FloatField(default=0)
    number_of_ratings = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Review(models.Model):
    review_user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=256)
    watchlist = models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name='reviews')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + " | "+ self.watchlist.title 