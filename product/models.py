from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
import string
from django.utils.html import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from customer.models import Customer
from .category_filter import CATEGORY_DETAILS, CATEGORY_CHOICES
from utils.utils import compress_image_uploads

def product_image_directory(instance, filename):
    new_product_image = compress_image_uploads(filename)
    return f"{instance.__class__.__name__}/{instance.vend_id}/{new_product_image}"

def customer_review_image_directory(instance, filename):
    new_file = compress_image_uploads(filename)
    return f"{instance.__class__.__name__}/{instance.cid}/{new_file}"

# product
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=15, prefix="PROD-", alphabet=string.digits)
    title = models.CharField(max_length=100)
    description = RichTextUploadingField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand_name = models.CharField(max_length=100)
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
    img_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=string.digits, prefix="IMG-")
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to=product_image_directory)
    more_images = models.ImageField(upload_to=product_image_directory, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def image_url(self):
        return mark_safe('<img src="%s" width=50 heigh=50 />' % (self.image.url))
        
    image_url.short_description = "Product Image"
    
    class Meta:
        verbose_name_plural = "Images"

class Category(models.Model):    
    cat_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=string.digits, prefix="CATEG-")
    category_choice = models.CharField(choices=CATEGORY_CHOICES, max_length=50, default='--select--')
    sub_category_details = models.CharField(choices=CATEGORY_DETAILS.get(category_choice), max_length=50)
    name = models.CharField(max_length=150)
    description = RichTextUploadingField(null=True, blank=True)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Categories"

    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.category_choice
    
# product inventory
class Inventory(models.Model):
    inv_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=string.digits, prefix="INV-")
    quantity = models.PositiveIntegerField(default=0)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Inventories"

    def __repr__(self):
        return self.inv_id
    
    def __str__(self):
        return self.inv_id
    
# product discount
class Discount(models.Model):
    dis_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=string.digits, prefix="DIS-")
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
    
    def __str__(self):
        return self.name
    
# handles user orders
class ProductOrders(models.Model):
    ORDER_STATUS = {
        ('Pending', 'pending'),
        ('Completed', 'paid'),
        ('Ongoing', 'ongoing'),
        ('Cancelled', 'cancelled'),
        ('Returns & Refunds', 'refunds')
    }

    ord_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=string.digits, prefix="ORD-")
    item_number = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default="-------")
    created_at = models.DateTimeField(default=timezone.now)
    
    # linking to the customer model
    # links many to one
    user_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Orders"
        verbose_name_plural = "Orders"

    def __repr__(self):
        return "{} {}".format(self.user_id, self.ord_id)
        
    def __str__(self):
        return "{} {}".format(self.user_id, self.ord_id)
    
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
    rev_id = ShortUUIDField(unique=True, length=10, max_length=15, prefix='REV-', alphabet=string.digits)
    review_title = models.CharField(max_length=50, default='Great Product')
    review_screenshots = models.ImageField(upload_to=customer_review_image_directory, null=True, blank=True, default=None)
    review_text = models.CharField(max_length=1000, default='I love the product')
    review_rating = models.CharField(max_length=50, choices=RATINGS, default='------')
    created_at = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def review_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.review_screenshots.url))
    
    review_tag.short_description = "Image"

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

    def __repr__(self):
        return self.review_title
    
    def __str__(self):
        return self.review_title


# popular product model
# saves the most popular product category
class PopularProduct(models.Model):
    pop_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=string.digits, prefix="POP-")
    category = models.CharField(max_length=50)
    popularity_count = models.IntegerField(default=0)
    
    def __repr__(self):
        return "{} {}".format(self.pop_id, self.category)
        
    def __str__(self):
        return "{} {}".format(self.pop_id, self.category)