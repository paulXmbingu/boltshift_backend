from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
import string
from django.utils.html import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from .category_filter import CATEGORY_CHOICES


def product_image_directory(instance, filename):
    return f"{instance.__class__.__name__}/{instance.img_id}/{filename}"

def customer_review_image_directory(instance, filename):
    return f"{instance.__class__.__name__}/{instance.rev_id}/{filename}"

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
    category = models.OneToOneField('Category', on_delete=models.SET_NULL, null=True)
    # inventory
    inventory = models.ForeignKey('Inventory', on_delete=models.SET_NULL, null=True)
    # discount
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True)
    # images
    images = models.ForeignKey('ProductImage', on_delete=models.SET_NULL, null=True)

    def __repr__(self):
        return "{} {}".format(self.title, self.brand_name)
    
    def __str__(self):
        return "{} {}".format(self.title, self.brand_name)

# product image
class ProductImage(models.Model):
    img_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=string.digits, prefix="IMG-")
    image = models.ImageField(upload_to=product_image_directory)
    more_images = models.FileField(upload_to=product_image_directory, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = timezone.now()
    
    def image_url(self):
        return mark_safe('<img src="%s" width=50 heigh=50 />' % (self.image.url))
        
    image_url.short_description = "Product Image"
    
    class Meta:
        verbose_name_plural = "Images"
        
    def __str__(self):
        return "{}".format(self.image.url)
        
    def __repr__(self):
        return "{}".format(self.image.url)

# One product for one category
# Similarly one category for one product
class Category(models.Model):    
    cat_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=string.digits, prefix="CATEG-")
    category_choice = models.CharField(choices=CATEGORY_CHOICES, max_length=50, default='--select--')
    #sub_category_details = models.CharField(choices=return_category_details_tuple(category_choice), max_length=50)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Categories"

    def __repr__(self):
        return "{}".format(self.category_choice)
    
    def __str__(self):
        return "{}".format(self.category_choice)
    
# product inventory/ product stock
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
    name = models.CharField(max_length=100, help_text="e.g, Black Friday")
    discount_percent = models.DecimalField(decimal_places=2, max_digits=5)
    active = models.BooleanField(default=False)
    updated_at = timezone.now()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Discounts"

    def __repr__(self):
        return "{} {}".format(self.name, self.active)
    
    def __str__(self):
        return "{} {}".format(self.name, self.active)
    
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
    user_id = models.ForeignKey("customer.Customer", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Orders"
        verbose_name_plural = "Orders"

    def __repr__(self):
        return "{} {}".format(self.status, self.ord_id)
        
    def __str__(self):
        return "{} {}".format(self.status, self.ord_id)
    
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
    review_screenshots = models.FileField(upload_to=customer_review_image_directory, null=True, blank=True, default=None)
    review_text = models.CharField(max_length=1000, default='I love the product')
    review_rating = models.CharField(max_length=50, choices=RATINGS, default='------')
    created_at = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey("customer.Customer", on_delete=models.SET_NULL, null=True)
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