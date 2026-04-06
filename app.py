from flask import Flask, redirect, render_template, request, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

from routes.auth import auth_bp
from routes.items import items_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET")

jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(items_bp)

@app.get('/')
def root():
    return render_template('index.html')

@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/register')
def register():
    return render_template('register.html')

@app.get('/animals')
def animals():
    return render_template('animals.html')

@app.get('/add-animal')
def add_animal():
    return render_template('add-animal.html')

@app.get('/edit-animal/<id>')
def edit_animal(id):
    return render_template('edit-animal.html')

if __name__ == '__main__':
    app.run(debug=False)