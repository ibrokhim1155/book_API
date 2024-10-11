from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from product.models import Category, Product
from product.views.category import CategoriesDetailListApiView, CategoryDetailApiView




@receiver(post_save, sender=Category)
def clear_category_cache_on_save(sender, instance, **kwargs):
    cache.delete(CategoriesDetailListApiView.cache_key)


@receiver(post_delete, sender=Category)
def clear_category_cache_on_delete(sender, instance, **kwargs):
    cache.delete(CategoriesDetailListApiView.cache_key)


@receiver(post_save, sender=Category)
def clear_category_cache_on_save(sender, instance, **kwargs):
    cache.delete(CategoryDetailApiView.cache_key)


@receiver(post_delete, sender=Category)
def clear_category_cache_on_delete(sender, instance, **kwargs):
    cache.delete(CategoryDetailApiView.cache_key)





@receiver(post_save, sender=Product)
def clear_product_cache_on_save(sender, instance, **kwargs):
    cache.delete('products-list')


@receiver(post_delete, sender=Product)
def clear_product_cache_on_delete(sender, instance, **kwargs):
    cache.delete('products-list')