### Flight Routes System – Django Machine Test

A Django web application that manages airport routes, calculates travel durations, and finds relationships between flight nodes.

This project was developed as part of a Django Machine Test, extended with extra functional enhancements to demonstrate real-world design and development skills.

### Features
  ### Core Requirements

    Find the Nth Left or Right Node in a route.

    Find the Longest Node based on duration.

    Find the Shortest Node between two airports.

    Add Airport Routes using Django forms (airport code, position, and duration).

  ### Functional Enhancements

  Total Route Duration Calculation

    Automatically calculates the total duration (sum of all nodes’ durations) for each route.

  Auto-Increment Node Position

    Automatically assigns position numbers (last position + 1) when adding new nodes.

  Route Summary Page

    Displays a clean summary table for all routes, including:

    Route name

    Starting and ending airport

    Number of nodes

    Total duration

  Navigation Buttons

    Quick access buttons for “Create Route”, “Add Node”, and “View Summary” directly on the homepage.

### Tech Stack

Backend: Django 4.2+

Frontend: Django Templates + Bootstrap 5

Database: SQLite (default, can switch to MySQL/PostgreSQL)

Language: Python 3.10+

### Installation & Setup
1️) Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # windows

2️) Install dependencies
pip install -r requirements.txt


3️) Run migrations
python manage.py makemigrations
python manage.py migrate

4️) Create a superuser (optional)
python manage.py createsuperuser

5️) Start the development server
python manage.py runserver

Now visit → http://127.0.0.1:8000/

### Usage Guide
Action - URL -	Description
Home Page	- / - View all routes and nodes
Create Route - /create-route/	- Add a new route
Add Node -	/add-node/ -	Add a new airport node to a route
Nth Node Search -	/search-nth/ -	Find Nth left/right node
Longest Node -	/longest-nodes/ -	View the longest-duration node(s)
Shortest Between -	/shortest-between/ -	Find the shortest duration between two airports
Route Summary -	/route-summary/ -	View summary of all routes with total durations
