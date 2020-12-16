import unittest
import requests
import re
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Note as Note
from models import User as User
from models import Todo as Todo
from models import Comment as Comment
from models import Budget as Budget
from models import Housing as House

class FlaskTest(unittest.TestCase):
    def test_index(self):
        response = requests.get("http://127.0.0.1:5000/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<p>Use this site to maintain and organize your notes.</p>' in response.text, True)

    def test_notes_not_logged_in(self):
        response = requests.get("http://127.0.0.1:5000/notes")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        #self.assertEqual('<p>Please log in</p>' in response.text, True)
        self.assertEqual('Title' and 'Date' in response.text, True)

    def test_registration_page(self):
        response = requests.get('http://127.0.0.1:5000/register')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_login_and_logout_page(self):
        response = requests.get('http://127.0.0.1:5000/login')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

        # signing in with a normal account
        response = requests.post("http://127.0.0.1:5000/login/check", {"email": "normal2@uncc.edu", "password": "qwerty1"})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h2 id="header_welcome">Welcome normal user!</h2>' in response.text, True)
        # signing out of normal user
        response = requests.get("http://127.0.0.1:5000/logout")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h2 id="header_welcome">Welcome !</h2>' in response.text, True)

        # signing in with admin account
        response = requests.post("http://127.0.0.1:5000/login/check", {"email": "admin@uncc.edu", "password": "qwerty1"})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h2 id="header_welcome">Welcome admin user!</h2>' in response.text, True)

    # everything after this is log in tests
    def test_search(self):
        response = requests.post("http://127.0.0.1:5000/search", {"search": "Software Note Week 1"})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_budget_before(self):
        requests.post("http://127.0.0.1:5000/budget/update", {"subtotal":"100","housing":"10","phone":"10","electricity":"10","gas":"10","water":"10","streaming":"10","maintenance":"10","supplies":"10","internet":"10","other":"10"})
        response = requests.get("http://127.0.0.1:5000/budget");
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        requests.post("http://127.0.0.1:5000/budget/update", {"subtotal":"200","housing":"10","phone":"10","electricity":"10","gas":"10","water":"10","streaming":"10","maintenance":"10","supplies":"10","internet":"10","other":"10"})
        response = requests.get("http://127.0.0.1:5000/budget");
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_add_todo(self):
        response = requests.post("http://127.0.0.1:5000/todo/new", {"description":"Study for a math final!"})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    def test_delete_todo(self):
        response = requests.post("http://127.0.0.1:5000/todo/deleteAll")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_add_note(self):
        response = requests.post("http://127.0.0.1:5000/notes/new", {"title":"This is a title!","noteText":"This is a note!"})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('>This is a title!</a>' in response.text, True)

    def test_create_comment(self):
        response = requests.post("http://127.0.0.1:5000/comment/1", {"commentText":"This is a comment!"})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<p>This is a comment!</p>' in response.text, True)

    def test_delete_note(self):
        response = requests.post("http://127.0.0.1:5000/notes/delete/6")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_regex(self):
        strong_password = "Strong1!"
        medium_password = "Medium1"
        self.assertTrue(re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})", strong_password))
        self.assertTrue(re.search("^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})", medium_password))

if __name__ == " __main__":
    unittest.main()
