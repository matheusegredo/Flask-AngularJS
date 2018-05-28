from flask import Flask, request, jsonify, session, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/usuarios'

db = SQLAlchemy(app)

#Definindo as tabelas do banco de dados

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id =  db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    cpf = db.Column(db.String(20), unique=True)
    telefone = db.Column(db.String(20))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/js/main_controller.js')
def controller():
    return render_template('main_controller.js')
	
@app.route('/js/main_module.js')
def module():
    return render_template('main_module.js')
	
@app.route('/js/main_factory.js')
def factory():
    return render_template('main_factory.js')

@app.route('/users', methods=['GET'])
def get_all_users():
    
    users = User.query.all()
    
    output = []
    
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name']  = user.name
        user_data['password'] = user.password
        user_data['cpf'] = user.cpf
        user_data['telefone'] = user.telefone
        output.append(user_data)
   
    return jsonify({'users' : output}) 

@app.route('/users/<public_id>', methods=['GET'])
def get_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name']  = user.name
    user_data['password'] = user.password
    user_data['cpf'] = user.cpf
    user_data['telefone'] = user.telefone

    return jsonify({'user' : user_data})

@app.route('/users', methods=['POST'])
def create_user():
	
    data = request.get_json()
        
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=data['password'], cpf=data['cpf'], telefone=data['telefone'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message' : 'Usuario criado' })

@app.route('/users/<public_id>', methods=['PUT'])
def promote_user(public_id):
    
    data = request.get_json()

    user = User.query.filter_by(public_id=public_id).first()
	
    if not user: 
        return jsonify({'message' : 'Nenhum usuario encontrado' })
    	
    user.name = data['name']
    user.password = data['password']
    user.cpf = data['cpf']
    user.telefone = data['telefone']

    db.session.commit()

    return jsonify({'message' : 'Usuario atualizado'}) 

@app.route('/users/<public_id>', methods=['DELETE'])
def delete_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user: 
        return jsonify({'message' : 'Nenhum usuario encontrado' }) 

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'Usuario deletado' })

if __name__ == "__main__":
    app.run(debug=True)
