from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Snack
# Create your tests here.
class SnackTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()
        testuser2 = get_user_model().objects.create_user(
            username="testuser2", password="pass2"
        )
        testuser2.save() 

    

        test_snack = Snack.objects.create(
            name="chips",
            owner=testuser1,
            desc="for eating",
        )
        test_snack.save()

    def setUp(self) -> None:
         self.client.login(username="testuser1", password="pass")  

   
    def test_snacks_model(self):
        snack = Snack.objects.get(id=1)
        actual_owner = str(snack.owner)
        actual_name = str(snack.name)
        actual_desc = str(snack.desc)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "chips")
        self.assertEqual(
            actual_desc, "for eating"
        )

    def test_get_snack_list(self):
        url = reverse("snack_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        things = response.data
        self.assertEqual(len(things), 1)
        self.assertEqual(things[0]["name"], "chips")


    def test_auth_required_get(self):
        self.client.logout() 
        url = reverse("snack_list")  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_auth_required_post(self):
        self.client.logout() 
        url = reverse("create_list")  
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_owner_can_delete_thing(self):
        self.client.logout()
        self.client.login(username="testuser2", password="pass2")
        url = reverse("snack_detail",args=[1])  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_only_owner_can_update_thing(self):
        self.client.logout()
        self.client.login(username="testuser2", password="pass2")
        url = reverse("snack_detail",args=[1])  
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)