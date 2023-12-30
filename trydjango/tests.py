import os
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.password_validation import validate_password

class TryDjangoConfigTest(TestCase):
    def test_secret_key_strength(self):
        SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

        try:
            validate_password(SECRET_KEY)
        except Exception as e:
            self.fail(e)