from django.test import TestCase
from .models import Product, Category, Inventory, Discount

class ProductModelTest(TestCase):
    def setUp(self):
        # Create test data, such as a category, inventory, and discount
        self.category = Category.objects.create(category_choice='Automotive', name='Auto')
        self.inventory = Inventory.objects.create(quantity=10)
        self.discount = Discount.objects.create(name='Test Discount', discount_percent=0.1, active=True)

    def test_create_product(self):
        # Test creating a product instance
        product = Product.objects.create(
            title='Test Product',
            description='This is a test product.',
            price=20.0,
            category=self.category,
            inventory=self.inventory,
            discount=self.discount
        )

        # Check if the product instance is created successfully
        self.assertIsInstance(product, Product)

        # Check if the product fields are saved correctly
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.description, 'This is a test product.')
        self.assertEqual(product.price, 20.0)
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.inventory, self.inventory)
        self.assertEqual(product.discount, self.discount)

    def test_product_str_representation(self):
        # Test the __repr__ method of the Product model
        product = Product.objects.create(
            title='Test Product',
            description='This is a test product.',
            price=20.0,
            category=self.category,
            inventory=self.inventory,
            discount=self.discount
        )

        expected_repr = 'Test Product'
        self.assertEqual(repr(product), expected_repr)

    # Add more test cases as needed
