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
        self.assertTrue(
            User.objects.filter(username=valid_data["username"]).exists()
        )
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
        self.assertFalse(
            User.objects.filter(username=invalid_data["username"]).exists()
        )
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

    def test_failure_post_with_duplicated_user(self):

        User.objects.create_user(
            username="tester", email="tester@test.com", password="testpassword"
        )

        invalid_data = {
            "username": "tester",
            "email": "tester@test.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertEqual(User.objects.count(), 1)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "A user with that username already exists.",
            form.errors["username"],
        )

    def test_failure_post_with_invalid_email(self):
        invalid_data = {
            "username": "tester",
            "email": "invalidemail",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.initial_user_count)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertIn("Enter a valid email address.", form.errors["email"])

    def test_failure_post_with_too_short_password(self):
        invalid_data = {
            "username": "tester",
            "email": "test@test.com",
            "password1": "t",
            "password2": "t",
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.initial_user_count)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertIn(
            "This password is too short. "
            "It must contain at least 8 characters.",
            form.errors["password2"],
        )

    def test_failure_post_with_password_similar_to_username(self):
        invalid_data = {
            "username": "testingname",
            "email": "test@test.com",
            "password1": "testingname",
            "password2": "testingname",
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.initial_user_count)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertIn(
            "The password is too similar to the username.",
            form.errors["password2"],
        )

    def test_failure_post_with_only_numbers_password(self):
        invalid_data = {
            "username": "testingname",
            "email": "test@test.com",
            "password1": "123123123",
            "password2": "123123123",
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.initial_user_count)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertIn(
            "This password is entirely numeric.", form.errors["password2"]
        )

    def test_failure_post_with_mismatch_password(self):
        invalid_data = {
            "username": "testingname",
            "email": "test@test.com",
            "password1": "testpassword1",
            "password2": "testpassword2",
        }

        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.initial_user_count)

        form = response.context["form"]

        self.assertFalse(form.is_valid())
        self.assertIn(
            "The two password fields didn’t match.", form.errors["password2"]
        )


class TestHomePageView(TestCase):
    def setUp(self):
        self.url = reverse("home")

    def test_success_get_home_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
