from django.db import models
from django.utils import timezone
from product.models import Product, PopularProduct
from collections import Counter
import cv2
import numpy as np
from sklearn.decomposition import PCA

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
        
        
# File Compressor for the uploaded images
# Shrinks the size of the images while retaining the quality
def compress_image_uploads(loaded_image):
    # converting the image color
    img = cv2.cvtColor(cv2.imread(loaded_image), cv2.COLOR_BGR2RGB)
    
    # destructing and reconstruction of the compressed image
    r, g, b = cv2.split(img)
    
    # calculating RGB pixels
    r, g, b = r / 255, g / 255, b / 255
    
    # shrinking the image components while retaining the original value
    pca_components = 200

    # reducing the red component
    pca_r = PCA(n_components=pca_components)
    reduced_r = pca_r.fit_transform(r)

    # reducing the green component
    pca_g = PCA(n_components=pca_components)
    reduced_g = pca_g.fit_transform(g)

    # reducing the blue component
    pca_b = PCA(n_components=pca_components)
    reduced_b = pca_b.fit_transform(b)

    combined = np.array(
        [reduced_r, reduced_b, reduced_g]
    )

    # reconstructing the components
    reconstructed_r = pca_r.inverse_transform(reduced_r)
    reconstructed_g = pca_g.inverse_transform(reduced_g)
    reconstructed_b = pca_b.inverse_transform(reduced_b)

    # reconstructing the image after compression
    img_reconstructed = (cv2.merge((reconstructed_r, reconstructed_g, reconstructed_b)))

    return img_reconstructed