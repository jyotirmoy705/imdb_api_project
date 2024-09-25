from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from imdb_app import models

class StreamTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'testuser', password='Password@123')
        self.token = Token.objects.create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token '+ self.token.key)
    def test_StreamPlatform(self):
        response = self.client.get(reverse('stream-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_StreamPlatform_create(self):
        data = {
            'name': 'Netflix',
            'description': 'Watch movies and TV shows.',
            'website': 'http://www.netflix.com'
        }
        response = self.client.post(reverse('stream-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class WatchlistTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'testuser', password='Password@123')
        self.token = Token.objects.create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token '+ self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name = 'Netflix', about = '# platform', website = 'http://www.netflix.com')
        self.watchlist = models.Watchlist.objects.create(title = 'Test watch', description = 'test desc', active = True, platform = self.stream)
        self.review = models.Review.objects.create(watchlist = self.watchlist, rating = 5, description = 'nice movie', reviewer = self.user)
        
    def test_Watchlist(self):
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_Watchdeetails(self):
        response = self.client.get(reverse('watchdetail', args = (self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Watchlist.objects.count(), 1)
        self.assertEqual(models.Watchlist.objects.get().title, 'Test watch')
    
    def test_WatchlistCreate(self):
        data = {
            'title': 'New Watchlist',
            'description': 'New watchlist description',
            'active': True,
            'platform': self.stream
        }
        response = self.client.post(reverse('watchlist'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'testuser', password='Password@123')
        self.token = Token.objects.create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token '+ self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name = 'Netflix', about = '# platform', website = 'http://www.netflix.com')
        self.watchlist = models.Watchlist.objects.create(title = 'Test watch', description = 'test desc', active = True, platform = self.stream)
        self.review = models.Review.objects.create(watchlist = self.watchlist, rating = 5, description = 'nice movie', reviewer = self.user)
        
    def test_Reviewlist(self):
        response = self.client.get(reverse('review', args = (self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_reviewcreate(self):
        data = {
            'reviewer': self.user.username,
            'rating': 5,
            'description': 'Great movie!',
            'watchlist': self.watchlist.pk
        }
        response = self.client.post(reverse('review-create', args = (self.watchlist.id,)), data)
        try:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        except:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
    def test_Watchlistwisereview(self):
        response = self.client.get(reverse('watchlistwisereview', args = (self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)