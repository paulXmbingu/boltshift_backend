![Boltshift Marketplace Project Cover](https://paulmbingu.imgix.net/Github%20Back-end%20Codebase%20File%20Cover.png?fit=max&w=1344&h=668&dpr=2&q=50&auto=format%2Ccompress)

# Boltshift Marketplace Backend

Welcome to the backend repository of Boltshift Marketplace – an online e-commerce platform built using Django. This repository contains the server-side code responsible for handling various aspects of the platform.

# Figma Design & Prototype

**Viewing Prototype in Figma:**
Control or Command-Click the buttons below to access the interactive prototype in Figma instantly. Explore the design by interacting with its elements. If you have any questions or encounter any issues, please don't hesitate to reach out to the designers in the Core Engineering Team for assistance (See credits list below). Your engagement with the prototype is appreciated!

[![Design](https://img.shields.io/badge/Design-Ctrl%20or%20Cmd%20Click-c644a3?style=flat)](https://www.figma.com/file/0NuM2ZQjyX4Nvatd58oMMM/Boltshift?type=design&node-id=1411%3A11643&mode=dev) [![Prototype](https://img.shields.io/badge/Prototype-Ctrl%20or%20Cmd%20Click-ff692e?style=flat)](https://www.figma.com/proto/0NuM2ZQjyX4Nvatd58oMMM/Boltshift?node-id=1663-14632&scaling=scale-down-width&page-id=1411%3A11643&starting-point-node-id=1663%3A14632&t=gYFeccmlX2jdKlsn-8&hide-ui=1)

![Boltshift Marketplace Product Cover Artwork](https://res.cloudinary.com/dmxl3sie6/image/upload/v1693654940/Boltshift%20Branding/Boltshift_Marketplace_Product_Cover_Artwork_q998tw.png)

## Prerequisites

- Python 3.x
- Virtual environment (recommended)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/Excite-Innovation-Company/Boltshift-Backend.git
   cd Boltshift-Backend
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Start the development server:
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
- Frontend Engineers: **Evelyne Atieno & Guantai John Paul**
- Backend Engineers: **Romeo Mureithi & Samuel Maingi**
- Android Engineers: **TBA**
- iOS Engineers: **TBA**
  
## Contributing

We welcome contributions to enhance the Boltshift Marketplace backend. To contribute, follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature/fix: `git checkout -b feature-name`
3. Make your changes and commit them.
4. Push your changes to your fork: `git push origin feature-name`
5. Open a pull request on the original repository.

## Support

For any questions or issues, feel free to contact our team at support@boltshiftmarketplace.com.

Happy coding!
