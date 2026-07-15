from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Alat Pay fields — only relevant when acting as a seller
    alatpay_subaccount_id = models.CharField(max_length=100, null=True, blank=True)
    alatpay_subaccount_ref = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.email