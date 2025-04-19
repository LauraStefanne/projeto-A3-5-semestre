from flask import Flask, render_template, request, redirect, session, url_for
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

@app.route('/ranking', methods=['GET', 'POST'])
def ranking():
    lista_ranking = []

    conn = criar_conexao()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True, buffered=True)

            if request.method == 'POST':
                nome = request.form['nome']
                pontuacao = request.form['pontuacao']

                # Verifica se o usuário existe
                query_usuario = "SELECT id FROM usuarios WHERE nome = %s"
                cursor.execute(query_usuario, (nome,))
                usuario = cursor.fetchone()

                if usuario:
                    # Insere na tabela ranking
                    query_inserir = "INSERT INTO ranking (id_usuario, pontuacao) VALUES (%s, %s)"
                    cursor.execute(query_inserir, (usuario['id'], pontuacao))
                    conn.commit()

            # Consulta todos os registros de ranking com nome do usuário
            consulta_ranking = """
                SELECT u.nome, r.pontuacao 
                FROM ranking r
                JOIN usuarios u ON r.id_usuario = u.id
            """
            #u é abreviação de usuarios e r é abreviação de ranking
            #join liga a tabela ranking e a tabela usuario para pegar o nome do usuario e o id do usuario
            cursor.execute(consulta_ranking)
            lista_ranking = cursor.fetchall()

        finally:
            conn.close()

    return render_template('ranking.html', lista_ranking=lista_ranking)



        
if __name__ == '__main__':
    app.run(debug=True)
