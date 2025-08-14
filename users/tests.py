from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestSignupView(TestCase):
    def setUp(self):
        self.url = reverse("account:signup")
        self.initial_user_count = User.objects.count()

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_success_post(self):
        valid_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, valid_data)

        # 1の確認 = tweets/homeにリダイレクトすること
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        # 2の確認 = ユーザーが作成されること
        self.assertTrue(User.objects.filter(username=valid_data["username"]).exists())
        # 3の確認 = ログイン状態になること
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_username(self):
        invalid_data = {
            "username": "",
            "email": "test@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=invalid_data["username"]).exists())
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["username"])

    def test_failure_post_with_empty_email(self):
        invalid_data = {
            "username": "tester",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertEqual(User.objects.count(), self.initial_user_count)
        self.assertIn("This field is required.", form.errors["email"])

    def test_failure_post_with_empty_password(self):
        invalid_data = {
            "username": "tester",
            "email": "tester@tester.com",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertEqual(User.objects.count(), self.initial_user_count)
        self.assertIn("This field is required.", form.errors["password1"])
        self.assertIn("This field is required.", form.errors["password2"])

    def test_failure_post_with_empty_form(self):
        invalid_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertEqual(User.objects.count(), self.initial_user_count)

        self.assertIn("This field is required.", form.errors["username"])
        self.assertIn("This field is required.", form.errors["email"])
        self.assertIn("This field is required.", form.errors["password1"])
        self.assertIn("This field is required.", form.errors["password2"])

