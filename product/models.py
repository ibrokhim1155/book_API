from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category')
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Group(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='group')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='groups')
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField()
    slug = models.SlugField(blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='products')
    users_like = models.ManyToManyField(User, related_name='products_likes', blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class AttributeKey(models.Model):
    key = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.key


class AttributeValue(models.Model):
    value = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.value


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='attributes')
    key = models.ForeignKey(AttributeKey, on_delete=models.SET_NULL, null=True, related_name='attribute_keys')
    value = models.ForeignKey(AttributeValue, on_delete=models.SET_NULL, null=True, related_name='attribute_values')

    def __str__(self):
        return f'{self.product}, {self.key}, {self.value}'


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='images')
    image = models.ImageField(upload_to='product', blank=True)  # default=None olib tashlandi
    is_primary = models.BooleanField(default=False)


class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.ZERO.value)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_comments')
    text = models.TextField()
    image = models.FileField(upload_to='comments', null=True, blank=True)

    def __str__(self):
        return f'{self.product} - {self.user}'
