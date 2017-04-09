from django.test import TestCase

from accounts.models import User, Wallet


class WalletTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test')
        cls.wallet = Wallet.objects.create(user=cls.user, savings=100.00)

    def test_str(self):
        assert str(self.wallet) == 'test'

    def test_update_savings(self):
        assert self.wallet.savings == 100.00

        self.wallet.update_savings(500.00)

        assert self.wallet.savings == 500.00


class UserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test')

    def test_str(self):
        assert str(self.user) == self.user.username
