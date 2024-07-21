![Boltshift Marketplace Project Cover](https://res.cloudinary.com/excit3/image/upload/v1716652242/Boltshift%20Branding/Github_Front-end_Codebase_File_Cover_doqfbz.png)

# Boltshift Marketplace Backend

Welcome to the backend repository of Boltshift Marketplace – an online e-commerce platform built using Django. This repository contains the server-side code responsible for handling various aspects of the platform.

## Prerequisites

- Python 3.x
- Virtual environment (recommended)

## Setup

1. **Clone the repository:**
   ```
   git clone https://github.com/Excite-Innovation-Company/Boltshift-Backend.git
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   pip install django
   ```

3. **Create and activate a virtual environment:**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Collecting all static files in one folder for easy rendering**
   ```
   python manage.py collectstatic
   ```
   
5. **Create a superuser (for first timers):**
   ```
   python manage.py createsuperuser
   ```
   
6. **Start the development server:**
   ```
   python manage.py runserver
   ```

## Usage

- Access the Django admin panel by navigating to `http://localhost:8000/admin/` and logging in with the superuser credentials.

- Interact with the API endpoints using tools like `curl` or API client applications like Postman.

## Project Structure

- `boltshift_backend/`: Main project directory.

   - `boltshift`: Base project folder. Contains:-
      - `settings.py`: Project settings including database configuration, authentication, and more.
      - `urls.py`: URL routing for the project:-
         - `admin/`: Admin panel
         - `customer/`: Home page, Orders, and more
         - `product/`: Product overview, product purchase, and more
         - `vendors/`: Vendor's panel, product tracking, income tracking

- `apps/`: Contains individual applications within the project.
  - `product/`: Application handling products and their details.
  - `vendors/`: Application for managing vendors/product owners.
  - `customer`: Application for managing customers/users

- `static/`: Static files like CSS, JavaScript, and images.
- `templates/`: HTML templates for rendering views.
- `requirements.txt`: List of required Python packages.

## Core Product Engineering Team

- Special Contributions: **Marion Ngayi & The Senjes Cuisine Team**
- Product Research & Design: **Paul Mbingu**
- Frontend Engineers: **Paul Mbingu & Felix Ouma**
- Backend Engineers: **Samuel Maingi & Paul Mbingu**
  

Happy coding!
