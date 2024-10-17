from flask import Flask, render_template, url_for, request, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import logging

login_manager = LoginManager()
load_dotenv('.env') #Utiliza o arquivo .env

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERMEGADIFICIL'
login_manager.init_app(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_banco'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

conexao = MySQL(app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('EMAILUSER') #Pega o user definido no arquivo env
app.config['MAIL_PASSWORD'] = os.getenv('EMAILSENHA') #Pega a senha definida no arquivo env
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False



#######################################################################


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    cursor = conexao.connection.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()  
    cursor.close()  
    return render_template('pages/index.html', usuarios=usuarios)

#######################################################################
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['pass']
        
        user = User.get_by_email(email)

        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return render_template('pages/tarefas.html')

    return render_template('pages/login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = generate_password_hash(request.form['pass'])
        cursor = conexao.connection.cursor()
        INSERT = 'INSERT INTO usuarios(email,senha) VALUES (%s, %s)'
        
        try:
            cursor.execute(INSERT, (email, senha)) 
            conexao.connection.commit()  
        except Exception as e:
            print(f"An error occurred: {e}")  
            conexao.connection.rollback()  
        finally:
            cursor.close()
        
       

        return render_template('pages/email_enviado.html')

    return render_template('pages/cadastro.html')

#######################################################################
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_tarefa():
    if request.method == 'POST':
        titulo = request.form['nome']
        conteudo = request.form['conteudo']
        data = request.form['data']
        limit_data = request.form['limit_data']

        
        cursor = conexao.connection.cursor()
        cursor.execute("INSERT INTO tarefas (usuario_id, titulo, conteudo, data, limit_data) VALUES (%s, %s, %s, %s, %s)", (current_user.id, titulo, conteudo, data, limit_data))



        
        conexao.connection.commit()
        cursor.close()
        
        return redirect(url_for('ver_tarefa')) 

    return render_template('pages/criar-tarefa.html')
#######################################################################
@app.route('/tarefas')
@login_required
def ver_tarefa():
    cursor = conexao.connection.cursor()  
    cursor.execute("SELECT * FROM tarefas WHERE usuario_id = %s", (current_user.id,)) 
    tarefas = cursor.fetchall() 
    cursor.close()

    return render_template('pages/tarefas.html', tarefas=tarefas)
#######################################################################

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
#######################################################################

@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    cursor = conexao.connection.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = %s", (id,))
    conexao.connection.commit()
    cursor.close()
    return redirect(url_for('ver_tarefa'))

#######################################################################

@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar(id):
    cursor = conexao.connection.cursor()
    cursor.execute('SELECT id, email FROM usuarios WHERE id = %s', (id,))
    user = cursor.fetchone()
    cursor.execute('SELECT id, titulo, conteudo FROM tarefas WHERE id = %s', (id,))
    tarefa = cursor.fetchone()
    
    if request.method == 'POST':
        if 'titulo' in request.form and 'conteudo' in request.form:
            titulo = request.form['titulo']
            conteudo = request.form['conteudo']
            data = request.form['data']
            limit_data = request.form['limit_data']
        
            cursor.execute('UPDATE tarefas SET titulo = %s, conteudo = %s, data = %s, limit_data = %s WHERE id = %s', (titulo, conteudo, data, limit_data, id))
            conexao.connection.commit()
            cursor.close()
            
            return redirect(url_for('ver_tarefa'))

    return render_template('pages/editar.html', tarefa=tarefa, user=user)