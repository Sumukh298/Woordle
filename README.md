# Guess the Word

A Django-based word guessing game developed as part of the OpenText project.

## Project Overview

Guess the Word is a web application with two types of users:

- **Player** – Registers, logs in, and plays the word guessing game.
- **Admin** – Manages the word database and views game reports.

The player is given a randomly selected five-letter word and can make up to five guesses to identify it.

## Features

### Player
- User registration and login
- Username and password validation
- Random five-letter word selection
- Maximum of 3 games per user per day
- Maximum of 5 guesses per game
- Color-based feedback for guesses:
  - 🟩 Green – Correct letter in the correct position
  - 🟧 Orange – Correct letter in the wrong position
  - ⬜ Grey – Letter is not present in the word
- Previous guesses displayed during the game
- Game completion and game-over handling

### Admin
- Add, edit, and delete words through Django Admin
- View daily game reports
- View reports for individual users
- Track words tried and correct guesses

## Tech Stack

- Python
- Django
- SQLite
- HTML
- CSS
- JavaScript
- Git & GitHub

## Project Structure

```text
Woordle/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── .gitignore
├── woordle/
├── guessgame/
├── templates/
└── static/
Setup
1. Clone the repository
git clone <your-github-repository-url>
cd Woordle
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment
Windows
venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Run migrations
python manage.py migrate
6. Start the development server
python manage.py runserver

Open the application at:

http://127.0.0.1:8000/
Admin Access

The application uses Django's built-in admin system.

Create an administrator account with:

python manage.py createsuperuser

Then access:

http://127.0.0.1:8000/admin/
Database

The project uses SQLite for data storage.

The database stores:

Users
Five-letter words
Games
Guesses
Game results
Version Control

Git is used for version control and GitHub is used to host the project source code.