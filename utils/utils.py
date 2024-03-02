from django.db import models
from django.utils import timezone
from product.models import Product, PopularProduct
from collections import Counter

# finds and saves the top product categories
def save_top_categories():
    # Get all products
    all_products = Product.objects.all()

    # Calculate category popularity count
    category_counts = Counter(product.category for product in all_products)

    # Find the top 5 categories
    top_categories = category_counts.most_common(5)

    # Save the top 6 categories to the PopularProduct model
    for category, count in top_categories:
        popular_product, created = PopularProduct.objects.get_or_create(category=category)
        popular_product.popularity_count = count
        popular_product.save()
    
"""
# A models mixin that helps in deleting a user's account data temporarily
# The deleted data is saved as a copy for a 30 day period before being deleted permanently
"""
class UserAccountMixin(models.Model):
    # saving the account deleted timezone
    deleted_at = timezone.now()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def undelete(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True