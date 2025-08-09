from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model

from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a payment entry in the database'

    def add_arguments(self, parser):
        parser.add_argument('user_email', type=str, help='Email of the user making the payment')
        parser.add_argument('amount', type=float, help='Amount of the payment')
        parser.add_argument('payment_method', type=str, choices=['cash', 'transfer'], help='Payment method')

    def handle(self, *args, **kwargs):
        user_email = kwargs['user_email']
        amount = kwargs['amount']
        payment_method = kwargs['payment_method']

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User with this email does not exist'))
            return

        payment = Payment.objects.create(
            user=user,
            amount=amount,
            payment_method=payment_method
        )

        self.stdout.write(self.style.SUCCESS(f'Payment of {payment.amount} created for user {user.email}'))
