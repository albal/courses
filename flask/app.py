from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Read environment variables
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')

# Construct the database connection string
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text)
    state = db.Column(db.String(255), default='Open')
    votes = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ip_address = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Merge(db.Model):
    __tablename__ = 'merges'
    id = db.Column(db.Integer, primary_key=True)
    from_course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    to_course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password, email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created!"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = []

    for user in users:
        users_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

    return jsonify({"users": users_list})

@app.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    new_course = Course(title=data['title'], summary=data['summary'])
    db.session.add(new_course)
    db.session.commit()

    # Convert the course to a dictionary or use a serialization method if available
    course_dict = {
        'id': new_course.id,
        'title': new_course.title,
        'summary': new_course.summary,
        'votes': new_course.votes
    }

    return jsonify({"course": course_dict}), 201

@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    courses_list = []

    for course in courses:
        courses_list.append({
            "id": course.id,
            "title": course.title,
            "summary": course.summary,
            "state": course.state,
            "votes": course.votes,
            "created_at": course.created_at,
            "updated_at": course.updated_at
        })

    return jsonify({"courses": courses_list})

@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found!"}), 404
    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Course deleted successfully!"}), 200

@app.route('/courses/<int:course_id>/upvote', methods=['POST'])
def upvote_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found!"}), 404

    course.votes += 1
    db.session.commit()

    return jsonify({"message": "Course upvoted!"}), 200

# Add more endpoints for reading, updating, and deleting...

if __name__ == "__main__":
#    db.create_all()  # To create tables based on the defined schema
    app.run(debug=True)

