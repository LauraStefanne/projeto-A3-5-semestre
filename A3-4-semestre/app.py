from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html') 

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
                return "Usuário cadastrado com sucesso!"
            except Error as e:
                return f"Erro ao inserir usuário: {e}"
        else:
            return "Erro na conexão com o banco de dados."
    
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
