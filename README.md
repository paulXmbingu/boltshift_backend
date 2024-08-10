![Boltshift Marketplace Project Cover](https://res.cloudinary.com/excit3/image/upload/v1721684091/Boltshift%20Branding/Github_Front-end_Codebase_File_Cover_doqfbz.png)

# Boltshift Marketplace Backend

Welcome to the backend repository of Boltshift Marketplace – an online e-commerce platform built using Django. This repository contains the server-side code responsible for handling various aspects of the platform.

## Setup

1. **Prerequisites**
   - Install latest version of [Python](https://www.python.org/downloads/)
   - Virtual environment (recommended)

2. **Clone the repository:**
   ```
   git clone https://github.com/Excite-Innovation-Company/Boltshift-Backend.git
   ```

3. **Install dependencies:**
   ```
   pip install django
   ```
   ```
   pip install -r requirements.txt
   ```

4. **Create and activate a virtual environment:**
   ```
   python3 -m venv venv
   ```
   ```
   source venv/bin/activate
   ```

5. **Collecting all static files in one folder for easy rendering**
   ```
   python manage.py collectstatic
   ```
   
6. **Create a superuser (for first timers):**
   ```
   python manage.py createsuperuser
   ```
   
7. **Start the development server:**
   ```
   python manage.py runserver
   ```

## Usage

- Access the Django admin panel by navigating to ```http://localhost:8000/admin/``` and logging in with the superuser credentials.

- Interact with the API endpoints using tools like `curl` or API client applications like Postman.


## Product Engineering Team

- Special Contributions: **Marion Ngayi & The Senjes Cuisine Team**
- Product Research & Design: **Paul Mbingu**
- Frontend Engineers: **Paul Mbingu & Felix Ouma**
- Backend Engineers: **Samuel Maingi & Paul Mbingu**
