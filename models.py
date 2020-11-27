from database import db

class Note(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    email = db.Column("email", db.String(100))
    def __init__(self, title, text, date, email):
        self.title = title
        self.text = text
        self.date = date
        self.email = email

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(100))
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Todo(db.Model):
    id = db.Column("id", db.Integer, primary_key=True )
    todoTitle = db.Column("todo title", db.String(100))

#class Task(db.Model):
    #id = db.Column("id")

class Budget(db.Model):
    id = db.Column("id", db.Integer, primary_key=True )

class Housing(db.Model):
    SIZE = 20
    id = db.Column("id", db.Integer, primary_key=True)
    mortgage = db.Column("mortgage", db.Float(SIZE))
    phone = db.Column("phone", db.Float(SIZE))
    electricity = db.Column("electricity", db.Float(SIZE))
    gas = db.Column("gas", db.Float(SIZE))
    water = db.Column("water", db.Float(SIZE))
    streaming = db.Column("streaming_services", db.Float(SIZE))
    maintenance = db.Column("maintenance", db.Float(SIZE))
    supplies = db.Column("supplies", db.Float(SIZE))
    internet = db.Column("internet", db.Float(SIZE))
    other = db.Column("other", db.Float(SIZE))
    email = db.Column("other", db.String(100))
    subtotal = db.Column("subtotal", db.Float(SIZE))

    def __init__(self, mortgage,phone, electricity, gas, water, streaming, maintenance,
                 supplies, internet, other, email):
        self.mortgage = mortgage
        self.phone = phone
        self.electricity = electricity
        self.gas = gas
        self.water = water
        self.streaming = streaming
        self.streaming = maintenance
        self.supplies = supplies
        self.internet = internet
        self.other = other
        self.email = email





