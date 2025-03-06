from django.test import TestCase
from .utility import update_clicks
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.core.cache import cache
import json
from .models import ShortenedURL
from asgiref.sync import sync_to_async


class ShortenURLTest(TestCase):
     """Unit tests for synchronous-URL-Shortener APIs."""

     def setUp(self):
           self.client = APIClient()
           self.url_object = ShortenedURL.objects.create(original_url="https://web.whatsapp.com/")
           self.shortened_url=self.url_object.shortened_code

     def tearDown(self):
        cache.clear()
     
     # Create URL Tests
     def test_success_url_creation(self):
          """ success Create shorten url and store original test """
          url = reverse("shorten_url")
          response = self.client.post(
               url,
               data=json.dumps({"original_url": "https://chatgpt.com/c/67c99684-5d64-8006-bf15-a47c930384c3"}),
               content_type="application/json",
               headers={"Accept": "application/json"}

            )
          self.assertEqual(response.status_code, status.HTTP_200_OK)
    
     def test_url_creation_failure_rate_limit_exceeded(self):
        """Test the API when the rate limit is exceeded."""
        url = reverse("shorten_url")
        for _ in range(3):
            response = self.client.post(
               url,
               data=json.dumps({"original_url": "https://chatgpt.com/c/67c99684-5d64-8006-bf15-a47c930384c3"}),
               content_type="application/json",
               headers={
                "Accept": "application/json"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(
               url,
               data=json.dumps({"original_url": "https://chatgpt.com/c/67c99684-5d64-8006-bf15-a47c930384c3"}),
               content_type="application/json",
               headers={"Accept": "application/json"}

            )
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(
            response.json()["detail"],
            "Too many attempts. Please try again later.",
        )

     def test_url_creation_faliure_invalid_body(self):
          url = reverse("shorten_url")
          response = self.client.post(
               url,
               data=json.dumps({"x_url": "https://chatgpt.com/c/67c99684-5d64-8006-bf15-a47c930384c3"}),
               content_type="application/json",
               headers={"Accept": "application/json"}

            )
          self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
          self.assertEqual(
            response.json()["original_url"],
            ['This field is required.'],
        )

#-----------------------------------------------------------------------------------------------------------------------------#
# Retrieve URL from Shorten one Tests
      
     def test_success_retrieve_url(self):
         url = reverse('redirect_url', kwargs={"shortened_url": self.shortened_url})
         response = self.client.get(
             url,
             content_type="application/json",
             headers={"Accept": "application/json"}
         )
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(
            response.json()["URL"],
            'https://web.whatsapp.com/',
        )
         
     def test_failed_retrieve_url_rate_limit(self):
         url = reverse('redirect_url', kwargs={"shortened_url": self.shortened_url})
         for _ in range(3):
            response = self.client.get(
                url,
                content_type="application/json",
                headers={"Accept": "application/json"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

         response = self.client.get(
                url,
                content_type="application/json",
                headers={"Accept": "application/json"}
            )
         self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
         self.assertEqual(
            response.json()["detail"],
            "Too many attempts. Please try again later.",
          )
         
     def test_failed_retrieve_url_not_found(self):
            url = reverse('redirect_url', kwargs={"shortened_url": "8000mn"})
            response = self.client.get(
                url,
                content_type="application/json",
                headers={"Accept": "application/json"}
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(
                response.json()["error"],
                'URL not found',
            )
#-------------------------------------------------------------------------------------------------------------------------------#
# Retrieve URL stats Tests
     def test_success_get_stats(self):
         retreive_url = reverse('redirect_url', kwargs={"shortened_url": self.shortened_url})
         url = reverse('stats', kwargs={"shortened_url": self.shortened_url})
         for _ in range(2):
            response = self.client.get(
                retreive_url,
                content_type="application/json",
                headers={"Accept": "application/json"}
            )
            # For Django tests run in transactional isolation, meaning that the Celery worker doesn't see changes made within a test.
            update_clicks(self.shortened_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

         response = self.client.get(
                url,
                content_type="application/json",
                headers={"Accept": "application/json"}
            )
         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(
            response.json()["clicks"],
            2,
        )
         
     def test_failed_get_stats_rate_limit(self):
         url = reverse('stats', kwargs={"shortened_url": self.shortened_url})
         for _ in range(3):
            response = self.client.get(
                url,
                content_type="application/json",
                headers={"Accept": "application/json"}
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
         response = self.client.get(
                url,
                content_type="application/json",
                headers={"Accept": "application/json"}
            )
         self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
         self.assertEqual(
            response.json()["detail"],
            "Too many attempts. Please try again later.",
          )
     def test_failed_get_stats_not_found(self):
          url = reverse('stats', kwargs={"shortened_url": 'ioqa'})
          response = self.client.get(
              url,
              content_type="application/json",
              headers={"Accept": "application/json"}
          )
          self.assertEqual(response.status_code, 404)
          self.assertEqual(
                response.json()["error"],
                'URL not found',
            )

         
           
            


        


    