from django.apps import AppConfig
from django.db.models.signals import post_migrate


class EldConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eld'

    def ready(self):
        from django.contrib.auth.models import User
        from rest_framework.authtoken.models import Token
        from .models import Driver

        def create_default_users(sender, **kwargs):
            from django.contrib.auth.models import User
            from rest_framework.authtoken.models import Token
            from .models import Driver

            default_users = [
                {"username": "claudwatari", "password": "password25", "car_registration_number": "KDZ 444Z"},
            ]

            for u in default_users:
                user, created = User.objects.get_or_create(username=u["username"])
                if created:
                    user.set_password(u["password"])
                    user.save()
                    print(f"Created user: {user.username}")

                Token.objects.get_or_create(user=user)

                # Safer driver creation
                if not hasattr(user, "driver"):
                    Driver.objects.create(user=user, car_registration_number=u["car_registration_number"])
                else:
                    print(f"Driver already exists for user: {user.username}")
            
        # signal only after all imports are ready
        post_migrate.connect(create_default_users, sender=self)

