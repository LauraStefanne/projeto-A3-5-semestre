from flask import Flask, render_template, request, redirect, session, url_for
from flask import json
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'laurinha'  # Chave muito secreta 

#conecta com o banco de dados
def criar_conexao():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='cadastroA3',
            user='root',
            password=''
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
    return None

#página inicial
@app.route('/')
def index():
    return render_template('index.html')

#  cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        conn = criar_conexao()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
                valores = (nome, email, senha)
                cursor.execute(query, valores)
                conn.commit()
                cursor.close()
                conn.close()
                
                # Após o cadastro redireciona para o jogo
                session['usuario'] = nome
                return redirect(url_for('jogo'))
            except Error as e:
                return f"Erro ao inserir usuário: {e}"
        else:
            return "Erro na conexão com o banco de dados."

    return render_template('cadastro.html')

#login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = criar_conexao()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True, buffered=True)  
                query = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
                cursor.execute(query, (email, senha))
                usuario = cursor.fetchone()

                if usuario:
                    session['usuario'] = usuario['nome']
                    return redirect(url_for('jogo'))
                else:
                    return "Email ou senha inválidos."
            except Error as e:
                return f"Erro no login: {e}"
            finally:
                cursor.close()
                conn.close()

    return render_template('login.html')

# página do jogo
@app.route('/jogo')
def jogo():
    return render_template('jogo.html')  

# Esqueci a senha
@app.route('/senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form['email']
        nova_senha = request.form['nova_senha']

        conn = criar_conexao()
        if conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE usuarios SET senha = %s WHERE email = %s"
                cursor.execute(query, (nova_senha, email))
                conn.commit()

                if cursor.rowcount == 0:
                    return "E-mail não encontrado."
                return "Senha alterada com sucesso. <a href='/login'>Ir para o login</a>"
            except Error as e:
                return f"Erro ao atualizar a senha: {e}"
            finally:
                cursor.close()
                conn.close()
    return render_template('senha.html')

        
if __name__ == '__main__':
    app.run(debug=True)