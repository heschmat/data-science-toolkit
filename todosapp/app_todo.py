# Using AJAX to send data asynchronously
import sys
from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
db_uri = 'postgres://postgres:huaamy@localhost:5432/todoapp'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key= True)
    description = db.Column(db.String(), nullable= False)
    completed = db.Column(db.Boolean, nullable= False, default= False)

    def __repr__(self):
        return f'<Todo {self.id}: {self.description}>'

# # Make sure that the tables are created for all the models.
# db.create_all()
# Since we are using migrations, we wont need db.create_all()
# rather, we want the migrations version to store everything,
# from db creation to schema modifications over time.

@app.route('/')
def index():
    data = Todo.query.all()
    return render_template('index_todo.html', data= data)

@app.route('/todos/create', methods=['POST'])
def create_todo():
    # Initialize the error & the response body.
    err = False
    ## The default session option for `expire_on_commit` is True.
    ## To not access the Todo() boject after commiting, we save the result
    ## in a dictionary, and we'll return the jsonify-ed version of it.
    body = {} 
    try:
        # Get the JSON that comes back from the AJAX request.
        data = request.get_json()
        description = data['description']
        todo = Todo(description = description)

        db.session.add(todo)
        db.session.commit()

        # Add the info to the body.
        body['description'] = todo.description
    except:
        err = True
        # If sth went wrong, rollback.
        db.session.rollback()
        print(sys.exc_info())
    finally:
        # Always close your session, no matter what happens.
        db.session.close()
    
    if not err:
        # Return a json object that includes the info.
        return jsonify(body)
    else: # if error
        # The route handler should always return something
        # or raise an intentional exception, in the case of an error.
        abort(500)
