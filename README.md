# Recipe Search Web Application

This is a Django-based web application that allows users to search for recipes, register, log in, edit their bio profile, and view recipe details integrated with the Spoonacular API.

## Features

- **Recipe Search:**  
  - Search for recipes using a central search bar.
  - Recipe results displayed in a grid with images and titles.
  
- **User Authentication:**  
  - Register, login, and logout functionality.
  - Extended user profile (UserProfile) for additional data (bio).
  
- **Profile Editing:**  
  - Users can edit their bio.

- **Admin Panel:**  
  - Manage recipes, categories, and user profiles via the Django admin interface.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Jamshaa/Project-Web-1st-Activity
   python -m venv venv # On Windows:
   python3 -m venv venv  # On MAC
   source venv/bin/activate # Both
   cd cooking
   pip install -r requirements.txt
   cd recipe-search
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser  # optional
   python manage.py runserver
   ```

## Running with Docker Compose

You can also run the application using Docker Compose:

```bash
docker-compose up --build
```

This will build and start the application along with any necessary dependencies.

## Authors

- Wissam Amer @wissamamer 
- Miriam Robert Ibrahim  
- Matteo Cataneo @Matyeo004
- Ibrahim Memic @Ibe1999
- Alessandro 
- Hamza @jamshaa 

