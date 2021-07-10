from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.urls import reverse
from django.contrib.auth.models import User

from watchmate_app import serializers
from watchmate_app import models

class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example',password='password')
        self.token = Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION = "Token "+ self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="BS Value",about="Blacksheep",website="https://www.blacksheep.com")

    def test_streamplatformcreate(self):
        data={
            "name":"BS Value",
            "about": "Blacksheep",
            "website":"https://www.blacksheep.com"
        }
        response = self.client.post(reverse('stream-platform-list-view'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse('stream-platform-list-view'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(reverse('stream-platform-detail-view',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

class WatchListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",about="#1 Platform", website="https://www.netflix.com")

        self.watchlist = models.WatchList.objects.create(platform=self.stream,title='Example movie',storyline='example',active = True)
    
    def test_watchlist_create(self):
        data = {
        "platform": self.stream,
        "title": "Example Movie",
        "storyline": "Example Story",
        "active": True
        }
        response = self.client.post(reverse('watch-list-view'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('watch-list-view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse('watch-detail-view',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)

class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",about="#1 Platform", website="https://www.netflix.com")

        self.watchlist = models.WatchList.objects.create(platform=self.stream,title='Example movie',storyline='example',active = True)

        self.watchlist2 = models.WatchList.objects.create(platform=self.stream,title='Example movie',storyline='example',active = True)

        self.review = models.Review.objects.create(review_user=self.user,watchlist=self.watchlist2,rating=3,description = "The beast",active=True)
    
    def test_review_create(self):
        data={
            "review_user" : self.user,
            "watchlist":self.watchlist,
            "rating" : 3,
            "description" : "The best",
            "active":True
        }
        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Review.objects.count(), 2)

    def test_review_create_unauthenticated(self):
        data={
            "review_user" : self.user,
            "watchlist":self.watchlist,
            "rating" : 3,
            "description" : "The best",
            "active":True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data={
            "review_user" : self.user,
            "watchlist":self.watchlist,
            "rating" : 5,
            "description" : "The best - Updated",
            "active":False
        }
        response = self.client.put(reverse('review-detail',args=(self.review.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(models.Review.objects.get().description, "The best - Updated")

    def test_review_list(self):
        response = self.client.get(reverse('review-list',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_list_ind(self):
        response = self.client.get(reverse('review-detail',args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



