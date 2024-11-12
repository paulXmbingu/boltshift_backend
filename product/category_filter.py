# Base Category choices
CATEGORY_CHOICES = {
    ('Automotive', 'Automotive'),
    ('Baby Products', 'Baby Products'),
    ('Beauty & Personal Care', 'Beauty & Personal Care'),
    ('Health & Household', 'Health & Household'),
    ('Home & Kitchen', 'Home & Kitchen'),
    ('Luggage', 'Luggage'),
    ("Men's Fashion", "Men's Fashion"),
    ("Women's Fashion", "Women's Fashion"),
    ('Pet Supplies', 'Pet Supplipythones')
}

# category details
CATEGORY_DETAILS = {
    'Automotive': ['Car Care', 'Electronics & Accessories', 'Exterior Accessories', 'Lights & Lightning Accessoires', 'Interior Accessoiries', 'Motocycle & Powersports', 'Oil & Fluids', 'Paint & Paint Supplies'],
    'Baby Products': ['Activity & Entertainment', 'Apparel & Accessories', 'Baby & Toddler', 'Toys Baby', 'Care Baby Stationery', 'Diapering Feeding Gifts', 'Nursery Potty Training', 'Pregnancy & Maternity Safety'],
    'Beauty & Personal Care': ['Makeup', 'Skin Care', 'Hair Care', 'Fragnance', 'Foot, Hand & Nail Care', 'Tools & Accessories', 'Shave & Hair Removal', 'Personal Care Oral Care'],
    'Health & Household': ['Baby & Child Care', 'Health Care', 'Household Supplies', 'Medical Supplies & Equipment', 'Oral Care', 'Personal Care', 'Sexual Wellness', 'Sports Nutrition'],
    'Home & Kitchen': ['Kids Home Store', 'Kitchen & Dining', 'Bedding', 'Bath', 'Furniture', 'Home Decor', 'Wall Art', 'Lighting & Ceiling Fans'],
    'Luggage': ['Carry-Ons', 'Backpacks', 'Garment Bags', 'Travel Totes', 'Luggage Sets', 'Laptop Bags', 'Suitcases', 'Kids Luggage'],
    "Men's Fashion": ['Shorts', 'Shirts', 'Activewear', 'Hoodies & Sweatshirts', 'Jeans', 'Pants', 'Pajamas & Robes', 'Occupational & Workwear'],
    "Women's Fashion": ['Clothin', 'Shoes', 'Jewelry', 'Watches', 'Handbags', 'Accessories', 'Lingerie', 'Filter Lable'],
    'Pet Supplies': ['Dogs', 'Cats', 'Fish & Aquatic Pets', 'Birds', 'Horses', 'Reptiles & Amphibians', 'Small Animals', 'Filter Lable']
}

# returns a tuple representation of sub_category
# given the category
def return_category_details_tuple(category):
    g = ()
    for category in CATEGORY_DETAILS.get(category):
        g += ((category, category.lower()),)
    return g