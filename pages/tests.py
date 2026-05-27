from django.test import TestCase


class ViewTests(TestCase):
    def test_about_page(self):
        """About page should respond with a success 200."""
        response = self.client.get("/about", follow=True)
        self.assertEqual(response.status_code, 200)
