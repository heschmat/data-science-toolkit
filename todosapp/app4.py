# Using AJAX to send data asynchronously
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db_uri = 'postgres://postgres:huaamy@localhost:5432/challenges'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


class Skill(db.Model):
    __tablename__ = 'data_skills'
    id = db.Column(db.Integer, primary_key= True)
    course_name = db.Column(db.String(), nullable= False)
    status = db.Column(db.Integer, nullable= False)
    num_projects = db.Column(db.Integer, nullable= False)

    def __repr__(self):
        """Data Representation."""
        return(
            f'<Skill {self.id}: status for {self.course_name}',
            f' is {self.status}/10.>'
        )


# Make sure that the tables are created for all the models.
db.create_all()

@app.route('/')
def index():
    data= Skill.query.all()
    return render_template('index4.html', data= data)


@app.route('/skills/create', methods= ['POST'])
def create_skill():
    data = request.get_json()
    name = data.get('course_name', '')
    status = data.get('status', 0)
    num_projects = data.get('num_projects', 0)

    data = {
        'course_name': name,
        'status': 0 if status == '' else int(status),
        'num_projects': 0 if num_projects == '' else int(num_projects)
    }

    skill_new = Skill(**data)
    db.session.add(skill_new)
    db.session.commit()

    # Return the results as json.
    res = jsonify({
        'course_name': name,
        'status': status,
        'num_projects': num_projects
    })
    return res
