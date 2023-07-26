from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import  Snack


# Create your tests here.

class SnackTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username='testuser1', password='pass')
        testuser1.save()

        test_thing = Snack.objects.create(
            name='flower', description="test desc ...")
        test_thing.save()

    def test_animes_model(self):
        snack= Snack.objects.get(id=1)
      
        actual_name = str(snack.name)
        actual_desc = str(snack.description)
        
        self.assertEqual(actual_name, "flower")
        self.assertEqual(actual_desc, "test desc ...")