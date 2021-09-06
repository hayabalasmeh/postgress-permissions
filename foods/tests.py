
from django.test import TestCase
from django.contrib.auth import get_user_model, logout
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from .models import Food

class FoodModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='tester_1',password='123')
        test_user.save()

        test_food = Food.objects.create(
            author = test_user,
            title = 'Yummy Food',
            recepi = 'All yummy food'
        )
        test_food.save()
        #Second user
        test_user_2 = get_user_model().objects.create_user(username='tester_2',password='123')
        test_user_2.save()

        test_food_2 = Food.objects.create(
            author = test_user_2,
            title = 'Yummy Banana',
            recepi = 'healthy recepi'
        )
        test_food_2.save()

    def test_foods_content(self):
        food = Food.objects.get(id=1)

        self.assertEqual(str(food.author), 'tester_1')
        self.assertEqual(food.title, 'Yummy Food')
        self.assertEqual(food.recepi, 'All yummy food')
        food = Food.objects.get(id=1)
        
        food_2 = Food.objects.get(id=2)
        self.assertEqual(str(food_2.author), 'tester_2')
        self.assertEqual(food_2.title, 'Yummy Banana')
        self.assertEqual(food_2.recepi, 'healthy recepi')


# Testing API
class APITest(APITestCase):
    "Checking if the user is Authenticated"
    def test_list(self):
        test_user = get_user_model().objects.create_user(username='tester_1',password='123')
        test_user.save()
        client = APIClient()
        logged = client.login(username='tester_1',password='123')
        response = client.get(reverse('foods_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK,logged)

    "Checking if the user is Not Authenticated"
    def test_list_not_logged(self):
       
        response = self.client.get(reverse('foods_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 


    "Checking if the user see details"
    def test_detail(self):
        """
        Test if api can detail the food recepi
        """

        test_user = get_user_model().objects.create_user(username='tester_1',password='123')
        test_user.save()

        test_post = Food.objects.create(
            author = test_user,
            title = 'Yummy Food',
            recepi = 'All yummy food'
        )
        test_post.save()
        client = APIClient()
        logged = client.login(username='tester_1',password='123')
        response = client.get(reverse('foods_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK,logged)
        self.assertEqual(response.data, {
            'id':1,
            'title': test_post.title,
            'recepi': test_post.recepi,
            'author': test_user.id,
            
        })
    "Checking if  the owner can delete"

    def test_delete_owner(self):
        """
        Test if api can detail the food recepi
        """

        test_user = get_user_model().objects.create_user(username='tester_1',password='123')
        test_user.save()

        test_food = Food.objects.create(
            author = test_user,
            title = 'Yummy Food',
            recepi = 'All yummy food'
        )
        test_food.save()
        test_user_2 = get_user_model().objects.create_user(username='tester_2',password='123')
        test_user_2.save()

        test_food_2 = Food.objects.create(
            author = test_user_2,
            title = 'Yummy Banana',
            recepi = 'healthy recepi'
        )
        test_food_2.save()
       
         
        client = APIClient()
        logged = client.login(username='tester_1',password='123')
        url = reverse('foods_detail', args=[1])
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,logged)   

    "Checking if the user other than the owner can update "

    def test_delete_non_owner(self):
        """
        Test if api can detail the food recepi
        """

        test_user = get_user_model().objects.create_user(username='tester_1',password='123')
        test_user.save()

        test_food = Food.objects.create(
            author = test_user,
            title = 'Yummy Food',
            recepi = 'All yummy food'
        )
        test_food.save()
        test_user_2 = get_user_model().objects.create_user(username='tester_2',password='123')
        test_user_2.save()

        test_food_2 = Food.objects.create(
            author = test_user_2,
            title = 'Yummy Banana',
            recepi = 'healthy recepi'
        )
        test_food_2.save()
       
         
        client = APIClient()
        logged = client.login(username='tester_2',password='123')
        url = reverse('foods_detail', args=[1])
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,logged)
     

    