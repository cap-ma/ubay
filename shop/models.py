from django.db import models
from django.db.models import Model,DateTimeField
from django.conf import settings
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.models import AbstractUser
from django.db import models 
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken


class BaseModel(Model):
    """Simply inherit this class to enable soft usage on a model.
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True, related_name='+')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True, related_name='+')

    class Meta:
        abstract = True

    created_at = DateTimeField(auto_now_add=True, null=True)
    modified_at = DateTimeField(auto_now=True, null=True)



class User(AbstractUser,BaseModel):
    first_name = models.CharField(_('First Name'), max_length=255, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=255, blank=True)
    username = models.CharField(_('User Name'), max_length=255, blank=True)
  
    phone_number = models.CharField(_('Phone number'), max_length=14, unique=True, null=True)

    objects = UserManager()

    USERNAME_FIELD='phone_number'
    REQUIRED_FIELDS=[]

    class Meta:
        verbose_name=_('User')
        verbose_name_plural=_("User")
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)

        }
    def __str__(self):
        return self.phone_number
    

class Category(BaseModel):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(BaseModel):
    title=models.CharField(max_length=255,null=True)
    image=models.ImageField(upload_to='media/')
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=20,decimal_places=2)
    is_active=models.BooleanField()
    quantity=models.IntegerField(blank=True,null=True)
    box=models.IntegerField(blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return self.title

class CartProduct(BaseModel):
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING,null=True)

    def __str__(self) -> str:
        return self.product.title
    
class Order(BaseModel):
    total_price=models.DecimalField(max_digits=20,decimal_places=2)

    def __str__(self):
        return self.pk
    
class OrderProduct(BaseModel):
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING,null=True)
    order=models.ForeignKey(Order,on_delete=models.DO_NOTHING,null=True)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=20,decimal_places=2)

    def __str__(self) -> str:
        return self.pk











