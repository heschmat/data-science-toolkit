import sys
from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
uri_db = 'postgres://postgres@localhost:5432/todoapp'
app.config['SQLALCHEMY_DATABASE_URI'] = uri_db
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory= 'migrations')


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key= True)
    description = db.Column(db.String(), nullable= False)
    completed = db.Column(db.Boolean, nullable= False, default= False)

    def __repr__(self):
        res = f'<Todo {self.id} {self.description}>'
        return res

# # Make sure that the tables are created for all the models.
# db.create_all()
# Since we are using migrations, we wont need db.create_all()
# rather, we want the migrations version to store everything,
# from db creation to schema modifications over time.

@app.route('/')
def index():
    # Always show the tasks chronologically.
    # Lower ids have been entered sooner.
    data= Todo.query.order_by('id').all()
    return render_template('index_todo.html', data= data)


# @app.route('/todos/create', methods=['POST'])
# def create_todo():
#     description = request.form.get('descriptioni', '')
#     todo = Todo(description= description)
#     db.session.add(todo)
#     db.session.commit()

#     return redirect(url_for('index'))

@app.route('/todos/create', methods=['POST'])
def create_todo():
    # Initialize the error & the response body.
    err = False
    ## The default session option for `expire_on_commit` is True.
    ## To not access the Todo() boject after commiting, save the result
    ## in a dictionary, return the jsonify-ed version of it.
    body = {} 
    try:
        # Get the JSON that comes back from the AJAX request.
        data = request.get_json()
        description = data['description']
        
        todo = Todo(description= description)
        db.session.add(todo)
        db.session.commit()
        # Add the info to the body.
        body['description'] = todo.description

    except:
        err = True
        # If sth goes wrong, rollback.
        db.session.rollout()
        print(sys.exc_info())
    finally:
        # In any case - success or failure- close the session.
        db.session.close()

    if not err:
        return jsonify(body)
    else:
        # N.B. The route handler should always return sth, or
        # or raise an intentional exception, in the case of an error.
        abort(400)

@app.route('/todos/<todo_id>/set-done', methods=['POST'])
def set_task_done(todo_id):
    try:
        is_done = request.get_json()['completed']
        task = Todo.query.get(todo_id)
        task.completed = is_done
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('index'))
