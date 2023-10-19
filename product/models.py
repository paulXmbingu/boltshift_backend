from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
from string import hexdigits
from django.utils.html import mark_safe

from customer.models import CustomUser

def product_directory_path(instance, filename):
    return f"vendor_{instance.vend_id}/{filename}"

def admin_image_directory(instance, filename):
    return f"{instance.cid}/{filename}"

# product
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="product-", alphabet=hexdigits)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)


    """
        # Foreign Keys / Table Relationships
    """
    # category
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    # inventory
    inventory = models.ForeignKey('Inventory', on_delete=models.SET_NULL, null=True)
    # discount
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True)

    def __repr__(self):
        return self.title

# product image
class ProductImage(models.Model):
    img_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=hexdigits, prefix="image-")
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to=product_directory_path)
    created_at = models.DateTimeField(default=timezone.now)
    
    def image_url(self):
        return mark_safe('<img src="%s" width=50 heigh=50 />', (self.image.url))
    
    class Meta:
        verbose_name_plural = "Images"


class Category(models.Model):
    # Base Category choices
    CATEGORY_CHOICES = {
        ('Automotive', 'Auto'),
        ('Baby Products', 'Baby'),
        ('Beauty & Personal Care', 'Beauty'),
        ('Health & Household', 'Health'),
        ('Home & Kitchen', 'Home'),
        ('Luggage', 'Luggage'),
        ("Men's Fashion", 'Men'),
        ("Women's Fashion", 'Women'),
        ('Pet Supplies', 'Pet')
    }

    # category details
    CATEGORY_DETAILS = {
        'Auto': ['Car Care', 'Electronics & Accessories', 'Exterior Accessories', 'Lights & Lightning Accessoires', 'Interior Accessoiries', 'Motocycle & Powersports', 'Oil & Fluids', 'Paint & Paint Supplies'],
    }

    # gets the sub product category based on the choosen category choices
    def get_category_details_choices(self):
        return [(subcat, subcat) for subcat in self.CATEGORY_DETAILS.get(self.category_choice, [])]
    
    cat_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=hexdigits, prefix="cat-")
    category_choice = models.CharField(choices=CATEGORY_CHOICES, max_length=50, default='--select--')
    #category_details = models.CharField(choices=get_category_details_choices, max_length=50)
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Categories"

    def __repr__(self):
        return self.name
    
# product inventory
class Inventory(models.Model):
    inv_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=hexdigits, prefix="inv-")
    quantity = models.PositiveIntegerField(default=0)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Inventories"

    def __repr__(self):
        return self.quantity
    
# product discount
class Discount(models.Model):
    dis_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=hexdigits, prefix="dis-")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    discount_percent = models.DecimalField(decimal_places=2, max_digits=5)
    #discount_img = models.ImageField()
    active = models.BooleanField(default=False)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Discounts"

    def __repr__(self):
        return self.name
    

class ProductOrders(models.Model):
    ORDER_STATUS = {
        ('Pending', 'pending'),
        ('Completed', 'paid'),
        ('Ongoing', 'ongoing'),
        ('Cancelled', 'cancelled')
    }
    ord_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=hexdigits)
    item_number = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default="-------")
    created_at = models.DateTimeField(default=timezone.now)
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Orders"
        verbose_name_plural = "Orders"

    def __repr__(self):
        return self.ord_id

    
# user product review 
# N/B: a review MUST be tied to the corresponding product, also the user
class ProductReview(models.Model):
    RATINGS = {
        ('⭐⭐⭐⭐⭐', 5),
        ('⭐⭐⭐⭐', 4),
        ('⭐⭐⭐', 3),
        ('⭐⭐', 2),
        ('⭐', 1),
    }
    rev_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix='review-', alphabet=hexdigits)
    review_title = models.CharField(max_length=50, default='Great Product')
    review_screenshots = models.ImageField(upload_to=admin_image_directory, null=True, blank=True, default=None)
    review_text = models.CharField(max_length=1000, default='I love the product')
    review_rating = models.CharField(max_length=50, choices=RATINGS, default='------')
    created_at = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def review_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />', (self.review_screenshots.url))
    
    review_tag.short_description = "Image"

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

    def __repr__(self):
        return self.review_title
