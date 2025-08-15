from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from api.models import Product, Store


# @receiver([post_save, post_delete], sender=Product)
# def invalidate_product_cache(sender, instance, **kwargs):
#     print("Clearing product cache")
#
#     cache.delete_pattern('*product_list*')

# @receiver([post_save], sender=Store)
# def