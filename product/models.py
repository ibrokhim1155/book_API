from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category/')

    def __str__(self):
        return self.title


class Group(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='group/')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='groups')

    def __str__(self):
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    slug = models.SlugField(null=True, blank=True, unique=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, related_name='products')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
