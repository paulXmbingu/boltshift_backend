from django.db import models
from shortuuid.django_fields import ShortUUIDField
import string
from django.utils.html import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from .category_filter import CATEGORY_CHOICES
from django.apps import apps



def product_image_directory(instance, filename):
    return f"{instance.__class__.__name__}/{instance.img_id}/{filename}"

def customer_review_image_directory(instance, filename):
    return f"{instance.__class__.__name__}/{instance.rev_id}/{filename}"

# categories
class Category(models.Model):

    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = RichTextUploadingField(max_length=1000)
    parent_id = models.ForeignKey('self', on_delete = models.SET_NULL, null = True, blank = False, related_name= 'subcategories') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category_choice = models.CharField(choices=CATEGORY_CHOICES, max_length=50, default='--select--')


    # sub_category_details = models.CharField(choices=return_category_details_tuple(category_choice), max_length=50)
    class Meta:
        verbose_name_plural = "Categories"

    def __repr__(self):
        return "{}".format(self.category_choice)
    
    def __str__(self):
        return "{}".format(self.category_choice)

    
    def __str__(self):
        return self.name
    
    def __repre__(self):
        return self.name

    

# Brands
class Brand(models.Model):
    brand_id = ShortUUIDField(unique=True, length=10, max_length=15, prefix="brand-", alphabet=string.digits)
    name = models.CharField(max_length = 100)
    description = RichTextUploadingField(max_length =1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.name

    def __repr__ (self):
        return self.name

# product
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=15, prefix="PROD-", alphabet=string.digits)
    name = models.CharField(max_length=100)
    description = RichTextUploadingField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default = 0)
    category = models.ForeignKey(Category, on_delete =models.SET_NULL, null = True)
    brand_name = models.CharField(max_length=100)
    brand_id = models.ForeignKey(Brand,on_delete = models.SET_NULL, null = True)
    feautured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    """
        # Foreign Keys / Table Relationships
    """
    # categories
    # categories = models.ManyToOneRel(Category, on_delete=models.SET_NULL,  null = True)
    
    # inventory
    # inventory = models.ForeignKey('Inventory', on_delete=models.SET_NULL, null=True, related_name= 'products')
    # discount
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True)
    # images
    images = models.ForeignKey('ProductImages', on_delete=models.SET_NULL, null=True, related_name='products')


    def __repr__(self):
        return "{} {}".format(self.title, self.brand_name)
    
    def __str__(self):
        return "{} {}".format(self.title, self.brand_name)

# product image
class ProductImages(models.Model):
    image_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=string.digits, prefix="IMG-")
    image = models.ImageField(upload_to=product_image_directory)
    more_images = models.FileField(upload_to=product_image_directory, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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
# class Category(models.Model):    
#     category_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=string.digits, prefix="CATEG-")
    
    
# product inventory/ product stock
class Inventory(models.Model):
    inventory_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=string.digits, prefix="INV-")
    quantity = models.PositiveIntegerField(default=0)
    location =  models.CharField(max_length = 255, null = True)
    product =models.ForeignKey(Product, on_delete= models.SET_NULL, null = True, related_name= 'inventory') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Inventories"

    def __repr__(self):
        return self.inventory_id, self.pid, self.name

    
    def __str__(self):
        return self.inventory_id, self.pid, self.name
    
# product discount
class Discount(models.Model):
    dis_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=string.digits, prefix="DIS-")
    name = models.CharField(max_length=100, help_text="e.g, Black Friday")
    discount_percent = models.DecimalField(decimal_places=2, max_digits=5)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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



    order_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=string.digits, prefix="ORD-")
    item_number = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default="-------")
    payment_status = models.CharField(max_length=50, default = 'NEW')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    # linking to the customer model
    # links many to one
    user_id = models.ForeignKey("customer.Customer", on_delete=models.SET_NULL, null=True)
    #  lazy import to avoid circular imports
    def get_customer(self):
        
        Customer = apps.get_model('customer', 'Customer')
        return Customer.objects.get(id=self.cid)
    
    class Meta:
        verbose_name = "Orders"
        verbose_name_plural = "Orders"

    def __repr__(self):
        return "{} {}".format(self.status, self.ord_id)
        
    def __str__(self):
        return "{} {}".format(self.status, self.ord_id)
    

# handles orderd items
class OrderedItems(models.Model):
    order_item_id = ShortUUIDField(unique= True, length =10, max_length=15, prefix = 'ORD_ITEM-',alphabet = string.digits)
    order = models.ForeignKey(ProductOrders, on_delete= models.SET_NULL, null = True, related_name= 'orders')
    pid = models.ForeignKey(Product, on_delete= models.SET_NULL, null = True, related_name= 'orderedproducts')
    quantity = models.PositiveIntegerField(default = 0)
    price = models.FloatField(default = 0.00)
    discount = models.FloatField(default = 0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ordered item"
        verbose_name_plural = "ordered items"

    def __str__(self):

        return self.order_item_id, self.product_id, self.price
    
    def __repr__(self):

        return self.order_item_id, self.product_id, self.price


    
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    popularity_id = ShortUUIDField(unique=True, length=10, max_length=15, alphabet=string.digits, prefix="POP-")
    category = models.CharField(max_length=50)
    popularity_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __repr__(self):
        return "{} {}".format(self.popularity_id, self.category)
        
    def __str__(self):
        return "{} {}".format(self.popularity_id, self.category)

class ProductTag(models.Model):
    tag_id = ShortUUIDField(unique = True, length = 10, max_length = 15, alphabet = string.digits, prefix = "Ptag-")
    name = models.CharField(max_length=255)
    # pid = models.ForeignKey(Product,on_delete =models.SET_NULL, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "product tag"

    class Meta:
        verbose_name_plural = "product_tag_mappings"

    def __str__(self):
        return self.pid, self.tag_id

    def __repr__(self):

        return self.pid, self.tag_id
    


class ProductTagMapping(models.Model):
    tag_id = models.ForeignKey(ProductTag, on_delete=models.SET_NULL, null = True, related_name="product_tag")
    pid = models.ForeignKey(Product,on_delete =models.SET_NULL, null = True, related_name= 'products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pid, self.tag_id
    

    def __repr__(self):

        return self.pid, self.tag_id


'wishlist'
class Wishlist(models.Model):
    wishlist_id = ShortUUIDField(unique=True, length =10,max_length= 15, alphabet = string.digits, prefix = "Wishlist-")
    def get_customer(self):
        
        Customer = apps.get_model('customer', 'Customer')
        return Customer.objects.get(id=self.cid)
    
    product_id = models.ForeignKey(Product, on_delete= models. SET_NULL , null=True)
    user_id = models.ForeignKey("customer.Customer", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductFeature(models.Model):
    feature_id = ShortUUIDField(unique=True, length = 10, max_length= 15, alphabet = string.digits, prefix = "feature -")
    name = models. CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductFeatureMappings(models.Model):
    product_id = models.ForeignKey(Product, on_delete= models.SET_NULL, null = True, related_name= 'product_features')
    feature_id = models.ForeignKey(ProductFeature, on_delete= models.SET_NULL, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    