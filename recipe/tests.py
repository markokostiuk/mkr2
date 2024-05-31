from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Recipe

class RecipeViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Створення тестових даних
        self.category1 = Category.objects.create(name='Appetizers')
        self.category2 = Category.objects.create(name='Desserts')

        for i in range(15):  # Створимо 15 рецептів для випадкового вибору
            Recipe.objects.create(
                title=f'Recipe {i + 1}',
                description='Test description',
                instructions='Test instructions',
                ingredients='Test ingredients',
                category=self.category1
            )

        for i in range(5):  # Створимо 5 рецептів для іншої категорії
            Recipe.objects.create(
                title=f'Dessert Recipe {i + 1}',
                description='Test description',
                instructions='Test instructions',
                ingredients='Test ingredients',
                category=self.category2
            )

    def test_main_view_status_code(self):
        """
        Test that the main view returns a status code of 200.
        """
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_main_view_template(self):
        """
        Test that the main view uses the 'main.html' template.
        """
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, 'main.html')

    def test_main_view_context(self):
        """
        Test that the main view context contains 10 recipes.
        """
        response = self.client.get(reverse('main'))
        self.assertIn('recipes', response.context)
        self.assertEqual(len(response.context['recipes']), 10)

    def test_main_view_content(self):
        """
        Test that the main view contains 'Recipe' and 'Test description' in the content.
        """
        response = self.client.get(reverse('main'))
        self.assertContains(response, 'Recipe')
        self.assertContains(response, 'Test description')

    def test_main_view_empty(self):
        """
        Test that the main view context is empty when there are no recipes.
        """
        Recipe.objects.all().delete()
        response = self.client.get(reverse('main'))
        self.assertEqual(len(response.context['recipes']), 0)

    def test_category_detail_view_status_code(self):
        """
        Test that the category detail view returns a status code of 200 for a valid category.
        """
        response = self.client.get(reverse('category_detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_view_template(self):
        """
        Test that the category detail view uses the 'category_detail.html' template.
        """
        response = self.client.get(reverse('category_detail', args=[self.category1.id]))
        self.assertTemplateUsed(response, 'category_detail.html')

    def test_category_detail_view_context(self):
        """
        Test that the category detail view context contains the correct category and recipes.
        """
        response = self.client.get(reverse('category_detail', args=[self.category1.id]))
        self.assertIn('category', response.context)
        self.assertIn('recipes', response.context)
        self.assertEqual(response.context['category'], self.category1)
        self.assertEqual(len(response.context['recipes']), 15)

    def test_category_detail_view_empty(self):
        """
        Test that the category detail view context is empty when there are no recipes in the category.
        """
        Recipe.objects.filter(category=self.category1).delete()
        response = self.client.get(reverse('category_detail', args=[self.category1.id]))
        self.assertEqual(len(response.context['recipes']), 0)

    def test_category_detail_view_404(self):
        """
        Test that the category detail view returns a 404 status code for a non-existent category.
        """
        response = self.client.get(reverse('category_detail', args=[999]))
        self.assertEqual(response.status_code, 404)
