from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

class CustomUserTests(TestCase):
    full_name = "user full name"
    country= "usa"
    city= "texas"
    detailed_address=  "somewhere"

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@test.com',
            full_name = self.full_name,
            country= self.country,
            city= self.city,
            detailed_address=  self.detailed_address,
            password='testpass123'
        )

        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.full_name, "user full name")
        self.assertEqual(user.country, 'usa')
        self.assertEqual(user.city, 'texas')

        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.add_food)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='testadmin@testadmin.com',
            full_name = self.full_name,
            country= self.country,
            city= self.city,
            detailed_address=  self.detailed_address,
            password='testpass123'
        )
        self.assertEqual(admin_user.email, 'testadmin@testadmin.com')
        self.assertEqual(admin_user.full_name, "user full name")
        self.assertEqual(admin_user.country, 'usa')
        self.assertEqual(admin_user.city, 'texas')

        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertFalse(admin_user.add_food)


class SignupTests(TestCase): 
    email = 'newuser@email.com'
    full_name = "user full name"
    country = "usa"
    city = "texas"
    detailed_address = "3313 st12 no05"
    password = "testuser1234"

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign Up')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
            self.full_name, self.email, self.country, self.city, self.detailed_address, self.password)

        self.assertEqual(get_user_model().objects.all().count(), 1)

        self.assertEqual(get_user_model().objects.all()
                         [0].email, self.email)
                         
        self.assertEqual(get_user_model().objects.all()
                         [0].full_name, "user full name")       
                  