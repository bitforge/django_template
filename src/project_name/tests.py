from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from account import models as accounts
from translations import models as translations
from {{ project_name }} import models


class SmokeTest(TestCase):
    """
    Basic smoke tests to verify the project setup works end to end.
    """

    @classmethod
    def setUpTestData(cls):
        cls.admin = accounts.User.objects.create_superuser('admin@example.com', 'secret-pw-123')

    def setUp(self):
        self.api = APIClient()

    def test_user_manager(self):
        user = accounts.User.objects.create_user('Jane@EXAMPLE.com', 'secret-pw-123')
        self.assertEqual(user.email, 'Jane@example.com')
        self.assertEqual(user.display_name, 'Jane')
        self.assertFalse(user.is_staff)
        self.assertTrue(self.admin.is_superuser)

    def test_index_redirects_to_admin(self):
        response = self.client.get('/')
        self.assertRedirects(response, reverse('admin:index'), target_status_code=302)

    def test_admin(self):
        response = self.client.get(reverse('admin:login'))
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.admin)
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        for model in ['account_user', '{{ project_name }}_entry', 'translations_group']:
            response = self.client.get(reverse(f'admin:{model}_changelist'))
            self.assertEqual(response.status_code, 200, model)

    def test_health_check(self):
        accounts.User.objects.all().delete()  # An empty database is healthy too
        response = self.api.get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'db_up': True, 'storage_up': True, 'cache_up': True})

    def test_api_schema(self):
        response = self.api.get(reverse('schema'))
        self.assertEqual(response.status_code, 200)

    def test_jwt_login(self):
        response = self.api.post(
            reverse('token_obtain_pair'),
            {'email': 'admin@example.com', 'password': 'secret-pw-123'},
        )
        self.assertEqual(response.status_code, 200)
        self.api.credentials(HTTP_AUTHORIZATION=f'Bearer {response.json()["access"]}')
        response = self.api.get(reverse('user-me'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], 'admin@example.com')

    def test_api_errors_are_problem_json(self):
        response = self.api.get(reverse('user-me'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response['Content-Type'], 'application/problem+json')
        self.assertEqual(response.json()['status'], 403)

    def test_entries_api(self):
        models.Entry.objects.create(title='Hello', slug='hello')
        self.api.force_authenticate(self.admin)
        response = self.api.get(reverse('entries-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([e['slug'] for e in response.json()], ['hello'])

    def test_templates_api(self):
        models.Template.objects.create(title='Welcome', slug='welcome', head='Hi', body='**Hello**')
        self.api.force_authenticate(self.admin)
        response = self.api.get(reverse('get_template', kwargs={'slug': 'welcome'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['body'], '**Hello**')

    def test_translations_api(self):
        group = translations.Group.objects.create(name='General', key='general')
        translations.Text.objects.create(group=group, key='hello', de='Hallo', en='Hello')
        response = self.api.get(reverse('get-translations', kwargs={'lang': 'de'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'general': {'hello': 'Hallo'}})
