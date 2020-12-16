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
from models import Comment as Comment
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
user_log = []
budget_error = False

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
def index():
    all_notes = db.session.query(Note).all()
    return render_template('index.html', user=a_user, notes=all_notes)

@app.route('/notes')
def get_notes():
    #a_user = db.session.query(User).filter_by(email=a_user.email).one()
    my_notes = []

    if a_user:
        my_notes = db.session.query(Note).filter_by(email=a_user.email).all()

    return render_template('notes.html', notes=my_notes, user=a_user)

@app.route('/search', methods=['GET', 'POST'])
def search():
    all_notes = db.session.query(Note).all()
    search = request.form['search'].lower()

    filtered_all_List = []
    filtered_my_List = []

    for note in all_notes:
        if search in note.title.lower():
            filtered_all_List.append(note)

    if a_user:
        my_notes = db.session.query(Note).filter_by(email=a_user.email).all()
        for note in my_notes:
            if search in note.title.lower():
                filtered_my_List.append(note)

    global user_log
    user_log.append("User searched for '" + search + "'");
    return render_template('search.html', all_notes=filtered_all_List, my_notes=filtered_my_List, user=a_user)

@app.route('/notes/<note_id>')
def get_note(note_id):
    my_note = db.session.query(Note).filter_by(id=note_id).one()

    my_note_comment = db.session.query(Comment).filter_by(noteId=note_id).all()

    return render_template('note.html', comments=my_note_comment, note=my_note, user=a_user)

@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    my_note = db.session.query(Note).filter_by(id=note_id).one()
    db.session.delete(my_note)
    db.session.commit()

    # delete comment from post
    all_note_comment = db.session.query(Comment).filter_by(noteId=note_id).all()
    for note in all_note_comment:
        db.session.delete(note)
        db.session.commit()

    global user_log
    user_log.append("User deleted note " + note_id);
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

        global user_log
        user_log.append("User edited note " + note_id);
        return redirect(url_for('get_notes'))
    else:
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
        global user_log
        user_log.append("User created new note");
        return redirect(url_for('get_notes'))
    else:
        return render_template('new.html', user=a_user)

# Add comment to note
@app.route('/comment/<note_id>', methods =['GET', 'POST'])
def add_comment(note_id):
    comment = request.form['commentText']

    newComment = Comment(comment, a_user.email, note_id)
    db.session.add(newComment)
    db.session.commit()

    global user_log
    user_log.append("User created new comment for note " + note_id);
    my_note = db.session.query(Note).filter_by(id=note_id).one()

    return redirect(url_for('get_note', note_id=note_id))

# Delete comment to note
@app.route('/comment/delete/comment=<comment_id>&note=<note_id>', methods =['POST'])
def delete_comment(comment_id, note_id):
    comment = db.session.query(Comment).filter_by(id=comment_id).one()
    db.session.delete(comment)
    db.session.commit()

    global user_log
    user_log.append("User deleted comment " + comment_id + " for note " + note_id);
    my_note = db.session.query(Note).filter_by(id=note_id).one()

    return redirect(url_for('get_note', note_id=note_id))


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
    newUser = User(name, email, password, 0)
    db.session.add(newUser)
    db.session.commit()

    house = House(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, email, 0)
    db.session.add(house)
    db.session.commit()
    return redirect(url_for('log_in'))

# App route Display todo
@app.route('/todo')
def get_todos():
    my_todo = False
    if a_user:
        print(my_todo)
        my_todo = db.session.query(Todo).filter_by(email=a_user.email).all()
        if len(my_todo) == 0:
            my_todo = False

    print(my_todo)
    return render_template('todos.html', todos=my_todo, user=a_user)

# App route update todo
@app.route('/todo/save', methods=['POST'])
def save_todos():
    print(request.form.getlist("complete"))

    return redirect(url_for('get_todos'))

# App route edit todo
@app.route('/todo/edit/<todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    todo = db.session.query(Todo).filter_by(id=todo_id).one()
    if request.method == 'POST' and a_user:
        todo.description = request.form['description']

        db.session.add(todo)
        db.session.commit()

        global user_log
        user_log.append("User updated todo " + todo_id);
        return redirect(url_for('get_todos'))
    else:
        return render_template('todo.html', user=a_user,todo=todo)

# App route create a new todo
@app.route('/todo/new', methods=['GET', 'POST'])
def new_todo():
    if request.method == 'POST' and a_user:
        description = request.form['description']
        email = a_user.email
        complete = 0

        newTodo = Todo(description, complete, email)
        db.session.add(newTodo)
        db.session.commit()

        global user_log
        user_log.append("User created todo");
        return redirect(url_for('get_todos'))
    else:
        return render_template('todo.html', user=a_user, todo=False)

# App route create a new todo
@app.route('/todo/deleteAll', methods=['GET', 'POST'])
def delete_all_todo():
    all_todo = db.session.query(Todo).filter_by(email=a_user.email).all()
    for todo in all_todo:
        db.session.delete(todo)
        db.session.commit()

    global user_log
    user_log.append("User deleted all todo");
    return redirect(url_for('get_todos'))

# App route create a new todo
@app.route('/todo/delete/<todo_id>', methods=['GET', 'POST'])
def delete_todo(todo_id):
    todo = db.session.query(Todo).filter_by(id=todo_id).one()
    db.session.delete(todo)
    db.session.commit()

    global user_log
    user_log.append("User deleted todo " + todo_id);
    return redirect(url_for('get_todos'))

# App route to display budget
@app.route('/budget', methods =['GET', 'POST'])
def get_budget():
    my_budget = False
    remaining = 0
    if a_user:
        my_budget = db.session.query(House).filter_by(email=a_user.email).one()
        remaining = my_budget.subtotal - (my_budget.mortgage + my_budget.phone + my_budget.electricity + my_budget.gas + my_budget.water + my_budget.streaming + my_budget.maintenance + my_budget.supplies + my_budget.internet + my_budget.other)

    return render_template('budget.html', budget=my_budget, user=a_user, remaining=remaining, error=budget_error)

# App route to log in
@app.route('/login')
def log_in():
    return render_template('login.html',  user=False, error = False)

# App route to check if user has account
@app.route('/login/check', methods =['GET', 'POST'])
def log_in_check():
    global a_user
    try:
        get_user = db.session.query(User).filter_by(email=request.form['email']).one()
        if get_user.password == request.form['password']:
            a_user = get_user
            global user_log
            user_log.append("User logged in");
            return redirect(url_for('index'))
    except:
        print("Error getting user from database :: user not found?")
        a_user = False
    return render_template('login.html',  user=False, error="Incorrect email or password. Please try again.")

# App route to log out
@app.route('/logout')
def log_out():
    global a_user
    a_user = False
    global user_log
    print(user_log)
    user_log = []
    return redirect(url_for('index'))

#helper for budget update
def helperMethodBudget(value):
    new_int = value
    new_int = new_int.replace('.', '')
    return new_int

@app.route('/budget/update', methods=['GET', 'POST'] )
def update_budget():
    # check method used for request
    global budget_error
    budget_error = False
    if request.method == 'POST':
        house = db.session.query(House).filter_by(email=a_user.email).one()

        house.subtotal = request.form['subtotal']
        if helperMethodBudget(house.subtotal).isnumeric() == False:
            print(house.subtotal)
            budget_error = "There was an error with your request."
        house.mortgage = request.form['housing']
        if helperMethodBudget(house.mortgage).isnumeric()== False:
            budget_error = "There was an error with your request."
        house.phone = request.form['phone']
        if helperMethodBudget(house.phone).isnumeric()== False:
            budget_error = "There was an error with your request."
        house.electricity = request.form['electricity']
        if helperMethodBudget(house.electricity).isnumeric()== False:
            budget_error = "There was an error with your request."
        house.gas = request.form['gas']
        if helperMethodBudget(house.gas).isnumeric()== False:
            budget_error = "There was an error with your request."
        house.water = request.form['water']
        if helperMethodBudget(house.water).isnumeric()== False:
            budget_error = "There was an error with your request."
        house.streaming = request.form['streaming']
        if helperMethodBudget(house.streaming).isnumeric()== False:
            budget_error = "There was an error with your request."
        house.maintenance = request.form['maintenance']
        if helperMethodBudget(house.maintenance).isnumeric()== False:
            budget_error = "There was an error with your request."
        house.supplies = request.form['supplies']
        if helperMethodBudget(house.supplies).isnumeric()== False:
            budget_error = "There was an error with your request."
        house.internet = request.form['internet']
        if helperMethodBudget(house.internet).isnumeric()== False:
            budget_error = "There was an error with your request."
        house.other = request.form['other']
        if helperMethodBudget(house.other).isnumeric()== False:
            budget_error = "There was an error with your request."

        print(budget_error)
        if budget_error:
            return redirect(url_for('get_budget'))

        db.session.add(house)
        db.session.commit()

        global user_log
        user_log.append("User updated budget ");
        return redirect(url_for('get_budget'))

@app.route('/test', methods =['GET', 'POST'])
def get_test():
    return '<h1>{}</h1>'.format(request.form['mortgage'])




app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
