import sys
from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql.expression import false


app = Flask(__name__)
uri_db = 'postgres://postgres:huaamy@localhost:5432/todoapp'
app.config['SQLALCHEMY_DATABASE_URI'] = uri_db
# FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds
# significant overhead and will be disabled by default in the future.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory= 'migrations')


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key= True)
    description = db.Column(db.String(), nullable= False)
    completed = db.Column(db.Boolean, nullable= False, default= False)
    # By default, db.ForeignKey has nullable = False
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable= False)

    def __repr__(self):
        res = f'<Todo {self.id}: {self.description} is {self.completed}>'
        return res


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(), nullable= False)
    # db.relationsip('ChildrenClassName',
    # backref= 'list' ## custom name, referencing what the parent name should be.
    # lazy= True)
    todos = db.relationship('Todo', backref= 'list', lazy= True)

    def __repr__(self):
        return f'<TodoList name:{self.name}, todos: {self.todos}>'

# # Make sure that the tables are created for all the models.
# db.create_all()
# Since we are using migrations, we wont need db.create_all()
# rather, we want the migrations version to store everything,
# from db creation to schema modifications over time.

# @app.route('/')
# def index():
#     # Always show the tasks chronologically.
#     # Lower ids have been entered sooner.
#     data= Todo.query.order_by('id').all()
#     return render_template('index_todo.html', data= data)


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
        list_id = data['list_id']
        
        todo = Todo(description= description, list_id= list_id)
        db.session.add(todo)
        db.session.commit()
        # Add the info to the body.
        body['id'] = todo.id
        body['description'] = todo.description
        body['completed'] = todo.completed

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
    err = False
    try:
        is_done = request.get_json()['completed']
        task = Todo.query.get(todo_id)
        task.completed = is_done
        db.session.commit()
    except:
        db.session.rollback()
        err = True
        print(sys.exc_info())
    finally:
        db.session.close()

    if err:
        abort(500)
    else:
        # Redirect to the function index()
        return redirect(url_for('index'))

@app.route('/todos/<todo_id>/delete-task', methods=['DELETE'])
def remove_task(todo_id):
    err = False
    try:
        task = Todo.query.get(todo_id)
        db.session.delete(task)
        # or: Todo.query.filter_by(id= todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        err = True
    finally:
        db.session.close()

    if err:
        abort(500)
    else:
        return jsonify({'success': True})

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    # Make sure the only todos visible will be per list_id.
    # Order the tasks time-wise.
    lists = TodoList.query.all()
    active_list = TodoList.query.get(list_id)
    tasks = Todo.query.filter_by(list_id= list_id).order_by('id').all()
    return render_template(
        'index_todo.html',
        lists= lists, active_list= active_list, tasks= tasks
    )


@app.route('/')
def index():
    # The homepage will be the tasks related to list_id = 1:
    # i.e., `Uncategorized` tasks.
    return redirect(url_for('get_list_todos', list_id= 1))

@app.route('/lists/create', methods=['POST'])
def create_list():
    err = False
    body = {}
    try:
        data = request.get_json()
        # Create the list.
        name = data['name']
        todolist = TodoList(name= name)
        db.session.add(todolist)
        db.session.commit()
        # Save the info in body.
        body['id'] = todolist.id
        body['name'] = todolist.name
    except:
        err = True
        db.session.rollback()
        print(sys.exc_info)
    finally:
        db.session.close()
    
    if err:
        abort(500)
    else:
        return jsonify(body)

@app.route('/lists/<list_id>/set-done', methods=['POST'])
def set_list_done(list_id):
    err = False

    try:
        list_tasks = TodoList.query.get(list_id)
        # A list is only done, when all the sub-tasks are done.
        for task in list_tasks.todos:
            task.completed = True
        
        db.session.commit()
    except:
        err = True
        db.session.rollback()
    finally:
        db.session.close()

    if err:
        abort(500)
    else:
        return '', 200
