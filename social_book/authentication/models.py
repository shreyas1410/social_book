from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


    


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username,email=email,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username,email, password, **extra_fields)

class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=100)
    public_visibility = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    groups = models.ManyToManyField(Group, related_name="custom_user_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
@receiver(post_save, sender = CustomUser)
def user_call_api(sender, instance, **kwargs):
    print("user created")
    print(sender, instance, kwargs)

class UploadedFile(models.Model):
    user = models.ForeignKey(CustomUser,related_name="authors", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# list = UploadedFile.objects.values('user__id').annotate(Count('user'))                
# >>> list
# <QuerySet [{'user__id': 5, 'user__count': 2}, {'user__id': 19, 'user__count': 1}]>

# list = CustomUser.objects.values('id').annotate(Count('id')) 
# >>> list
# <QuerySet [{'id': 11, 'id__count': 1}, {'id': 8, 'id__count': 1}, {'id': 19, 'id__count': 1}, {'id': 4, 'id__count': 1}, {'id': 21, 'id__count': 1}, {'id': 14, 'id__count': 1}, {'id': 3, 'id__count': 1}, {'id': 17, 'id__count': 1}, {'id': 22, 'id__count': 1}, {'id': 20, 'id__count': 1}, {'id': 10, 'id__count': 1}, {'id': 7, 'id__count': 1}, {'id': 1, 'id__count': 1}, {'id': 5, 'id__count': 1}, {'id': 18, 'id__count': 1}, {'id': 2, 'id__count': 1}, {'id': 16, 'id__count': 1}, {'id': 15, 'id__count': 1}, {'id': 6, 'id__count': 1}]>

# CustomUser.objects.aggregate(Max('id'))
# {'id__max': 22}
    
# >>> CustomUser.objects.aggregate(Avg('id')) 
# {'id__avg': 11.526315789473685}
    
# >>> CustomUser.objects.aggregate(Sum('id')) 
# # {'id__sum': Decimal('219')}
