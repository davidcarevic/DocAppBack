from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('User must have an email adress.')
        if not password:
            raise ValueError('User must have a password.')
        else:
            user = self.model(
                email = self.normalize_email(email),
            )
            user.email = email
            user.is_staff = is_staff
            user.is_active = is_active
            user.is_admin = is_admin
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff = True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff = True,
            is_admin = True
        )
        return user
