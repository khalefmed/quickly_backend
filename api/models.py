from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
import uuid
from cloudinary.models import CloudinaryField




class CustomUserManager(BaseUserManager):
    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', phone)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('username', phone)

        if not phone:
            raise ValueError('The mobile field must be set')

        user = self.model(phone=phone, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user


class User(AbstractUser):
    phone = models.IntegerField(unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    USER_TYPE_CHOICES = [
        ('simple', 'Simple'),
        ('traitor', 'Traitor'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    ]
    type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='simple')
    default_lang = models.CharField(max_length=5, default='fr')
    fcm_token = models.CharField(max_length=250, default='')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.phone}'

    def save(self, *args, **kwargs):

        if self.password:
            self.password = self.password

        super().save(*args, **kwargs)



class Vendor(models.Model):
    TYPE_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('pharmacie', 'Pharmacie'),
        ('epicerie', 'Epicerie'),
    ]
    image = CloudinaryField('image')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.name} - {self.type}'



class ItemVendor(models.Model):
    image = CloudinaryField('image')
    nom = models.CharField(max_length=100, null=True)
    prix = models.FloatField()
    vendor = models.ForeignKey(Vendor, related_name='vendor_items', on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f'{self.nom} - {self.prix}'





class Commande(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
        ('loading', 'Loading'),
        ('delivered', 'Delivered'),
    ]

    prix = models.FloatField()
    livraison = models.FloatField(default=0)
    code = models.CharField(max_length=100, default='', unique=True, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    location = models.TextField()
    phone = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    capture = CloudinaryField('image', blank=True, null=True)
    livreur = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='livreur')

    def save(self, *args, **kwargs):
        if not self.code:
            unique_code = uuid.uuid4().hex[:8].upper()
            self.code = f"CM{unique_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande {self.id} - {self.status} - {self.code}"




class ItemCommande(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='items')
    number = models.PositiveIntegerField()
    item = models.ForeignKey(ItemVendor, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"ItemCommande {self.id} - x{self.number}"




