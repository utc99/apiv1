Main libraries used:

Flask - for web server
Flask-Migrate - database migrations.
Flask-Script - support for writing external scripts used with db migrations.
Flask-RESTful - restful API library.
Flask-SQLAlchemy - support for SQLAlchemy ORM.
requests - API posts/gets.

Usage:

- Run first-setup.ps1 to install dependencies and create database.
- Start app.py application

POST http://127.0.0.1:5000/api/users

Input: 
{
	"first_name": "John",
	"lastname_name": "Smith",
	"birthday": "1989-01-01"
}

GET http://127.0.0.1:5000/api/users

{
    users {
            "id": 1, 
            "first_name": "John",
            "last_name": "Smith", 
            "birthday": "1989-01-01"
          }
}

GET http://127.0.0.1:5000/api/users?name=John