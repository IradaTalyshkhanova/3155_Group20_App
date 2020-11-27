# FLASK Tutorial 2 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Note as Note
from models import User as User
from models import Todo as Todo
from models import Budget as Budget
from models import Housing as House

app = Flask(__name__)     # create an app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# Setup models
with app.app_context():
    db.create_all()   # run under the app context

a_user = False

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
def index():
    return render_template('index.html', user=a_user)

@app.route('/notes')
def get_notes():
    #a_user = db.session.query(User).filter_by(email=a_user.email).one()
    my_notes = []

    if a_user:
        my_notes = db.session.query(Note).filter_by(email=a_user.email).all()

    return render_template('notes.html', notes=my_notes, user=a_user)

@app.route('/notes/<note_id>')
def get_note(note_id):
    #a_user = db.session.query(User).filter_by(email=a_user.email).one()

    my_note = db.session.query(Note).filter_by(id=note_id).one()

    return render_template('note.html', note=my_note, user=a_user)

@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    my_note = db.session.query(Note).filter_by(id=note_id).one()
    db.session.delete(my_note)
    db.session.commit()

    return redirect(url_for('get_notes'))

@app.route('/notes/edit/<note_id>', methods =['GET', 'POST'])
def update_note(note_id):
    if request.method == 'POST':
        title = request.form['title']

        text = request.form['noteText']
        note = db.session.query(Note).filter_by(id=note_id).one()

        note.title = title
        note.text = text

        db.session.add(note)
        db.session.commit()

        return redirect(url_for('get_notes'))
    else:
        #a_user = db.session.query(User).filter_by(email=a_user).one()

        my_note = db.session.query(Note).filter_by(id=note_id).one()

        return render_template('new.html', note=my_note, user=a_user)

@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
    # check method used for request
    if request.method == 'POST' and a_user:
        # get title data
        title = request.form['title']
        # get note data
        text = request.form['noteText']
        # create date stamp
        from datetime import date
        today = date.today()
        # format date mm/dd/yyy
        today = today.strftime("%m-%d-%Y")
        newEntry = Note(title, text, today, a_user.email)
        db.session.add(newEntry)
        db.session.commit()
        return redirect(url_for('get_notes'))
    else:
        return render_template('new.html', user=a_user)

# App route to register 
@app.route('/register')
def register():
    return render_template('register.html', user=a_user)

@app.route('/register/new', methods=['GET', 'POST'])
def register_account():
    # get name data
    name = request.form['name']
    # get note data
    email = request.form['email']
    # get note data
    password = request.form['password']
    # create user
    newUser = User(name, email, password)
    db.session.add(newUser)
    db.session.commit()

    house = House(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, email)
    db.session.add(house)
    db.session.commit()
    return redirect(url_for('index'))

# App route Display todo
@app.route('/todo')
def get_todos():
    my_todo = db.session.query(Todo).all()

    return render_template('todos.html', notes=my_todo, user=a_user)

# App route view specific todo
@app.route('/todo/<todo_id>')
def get_todo(todo_id):
    #a_user = db.session.query(User).filter_by(email=a_user.email).one()
    my_todo = db.session.query(Todo).filter_by(id=todo_id).one()

    return render_template('todo.html', note=my_todo, user=a_user)

# App route edit todo

# App route to display budget
@app.route('/budget', methods =['GET', 'POST'])
def get_budget():
    #a_user = db.session.query(User).filter_by(email=a_user.email).one()
    my_budget = False
    if a_user:
        my_budget = db.session.query(House).filter_by(email=a_user.email).one()

    return render_template('budget.html', budget=my_budget, user=a_user)

# App route to log in
@app.route('/login')
def log_in():
    return render_template('login.html',  user=False)

# App route to check if user has account
@app.route('/login/check', methods =['GET', 'POST'])
def log_in_check():
    global a_user
    try:
        get_user = db.session.query(User).filter_by(email=request.form['email']).one()
        if get_user.password == request.form['password']:
            a_user = get_user
            return redirect(url_for('index'))
    except:
        print("Error getting user from database :: user not found?")
        a_user = False
    return redirect(url_for('log_in'))

# App route to log out
@app.route('/logout')
def log_out():
    global a_user
    a_user = False
    return redirect(url_for('index'))

@app.route('/budget/update',methods=['GET', 'POST'] )
def update_budget():
    # check method used for request
    if request.method == 'POST':

        mortgage = request.form['mortgage']
        phone = request.form['phone']
        electricity = request.form['electricity']
        gas = request.form['gas']
        water = request.form['water']
        streaming = request.form['streaming']
        maintenance = request.form['maintenance']
        supplies = request.form['supplies']
        internet = request.form['internet']
        email = "nope"
        other = request.form['other']

        house = House(mortgage, phone, electricity, gas, water, streaming, maintenance, supplies, internet, other)

        #house = House(request.form['mortgage'], request.form['phone'], request.form['electricity'],
                      #request.form['gas'], request.form['water'], request.form['streaming'],
                      #request.form['maintenance'], request.form['supplies'], request.form['internet'],
                      #request.form['other'])
        db.session.add(house)
        db.session.commit()

        return redirect(url_for('get_budget'))
    else:
        #a_user = db.session.query(User).filter_by(email=a_user.email).one()
        a_house = db.session.query(House).all()
        return "There was an error"#render_template('budgetUpdate.html', user=a_user, house=a_house)

@app.route('/test', methods =['GET', 'POST'])
def get_test():
    return '<h1>{}</h1>'.format(request.form['mortgage'])




app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
