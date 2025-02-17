![Boltshift Marketplace Project Cover](https://res.cloudinary.com/excit3/image/upload/v1721684091/Boltshift%20Branding/Github_Front-end_Codebase_File_Cover_doqfbz.png)

# Boltshift Marketplace Backend
Welcome to the backend codebase of Boltshift Marketplace – built using Django. This repository contains the server-side code responsible for handling various aspects of the platform.

## Setup and Usage

1. **Clone the repository:**
   ```
   git clone https://github.com/paulXmbingu/boltshift_backend
   ```

2. **Create and activate the virtual environment:**
   ```
   python -m venv venv && source venv/bin/activate
   ```
   
3. **Install Django:**
   ```
   pip install django
   ```
   
4. **Install app requirements:**
   ```
   pip install -r requirements.txt
   ```
   
5. **Start the development server:**
   ```
   python manage.py runserver
   ```

### Usage

1. **Create a superuser (for first timers):**
   ```
   python manage.py createsuperuser
   ```

# Docker Setup
### Setup Application
1. Build and Run application
```
docker-compose up --build -d
```

### Restore Database
1. To backup your database
``` bash
./db/backup.sh
```
Do note that after any database change you backup the database again


## Features
- **User Authentication**: Secure user accounts and authentication to manage profiles and track order history.
- **Product Catalog**: A comprehensive listing of products, organized into categories for easy navigation.
- **Search and Filters**: Effortlessly find products using the search functionality & apply filters to narrow down choices.
- **Shopping Cart**: Add products to cart, review before purchasing, and easily adjust quantities.
- **Wishlist**: Curate shopping desires! Collect and save items they love—your personalized shopping inspiration.
- **Secure Payments**: Multiple payment options with enhanced security to ensure safe transactions.
- **Order Tracking**: Track the status of orders from purchase to delivery.
- **Responsive Design**: Enjoy a consistent experience across various devices, from smartphones to desktops.
- **Live Chat**: Connect with customer service representatives in real-time to address queries and resolve issues.

## Technologies
- **Figma**: Design & Prototyping
- **Miro**: Flowchart & Diagramming
- **Dovetail**: Research Analysis & Repository
- **Maze**: Usability Study
- **React.js**: Frontend Framework
- **CSS Modules**: Styling
- **React Router**: Routing
- **Redux**: State Management
- **tawk.to**: Live Chat
- **Django**: Backend Framework

## Product Engineering Team
- Special Contributions: **Marion Ngayi & The Senjes Cuisine Team**
- Product Research & Design: **Paul Mbingu**
- Frontend Engineers: **Paul Mbingu & Felix Ouma**
- Backend Engineers: **Samuel Maingi & Paul Mbingu**
