# Using AJAX to send data asynchronously
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
db_uri = 'postgres://postgres:huaamy@localhost:5432/challenges'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key= True)
    description = db.Column(db.String(), nullable= False)

    def __repr__(self):
        return f'<Todo {self.id}: {self.description}>'

# Make sure that the tables are created for all the models.
db.create_all()

@app.route('/')
def index():
    data = Todo.query.all()
    return render_template('index_todo.html', data= data)

@app.route('/todos/create', methods=['POST'])
def create_todo():
    # Get the JSON that comes back from the AJAX request.
    data = request.get_json()
    description = data['description']
    todo = Todo(description = description)

    db.session.add(todo)
    db.session.commit()

    # Instead of redirecting,
    # We want to return a json object that includes the info.
    res = jsonify({
        'description': todo.description
    })
    # return redirect(url_for('index'))
    return res
