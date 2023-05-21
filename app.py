import sqlite3
from flask import Flask, request, render_template, redirect

app = Flask(__name__)
DATABASE = 'funcionarios.db'

def criar_tabela():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            data_nascimento TEXT,
            salario REAL
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def listar_funcionarios():
    filtro_codigo = request.args.get('filtro_codigo', default='')
    filtro_nome = request.args.get('filtro_nome', default='')
    filtro_data_nascimento = request.args.get('filtro_data_nascimento', default='')
    filtro_salario = request.args.get('filtro_salario', default='')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = "SELECT * FROM funcionarios WHERE 1=1"

    if filtro_codigo:
        query += " AND id = {}".format(filtro_codigo)

    if filtro_nome:
        query += " AND nome LIKE '%{}%'".format(filtro_nome)

    if filtro_data_nascimento:
        query += " AND data_nascimento LIKE '%{}%'".format(filtro_data_nascimento)

    if filtro_salario:
        query += " AND salario like '%{}%'".format(filtro_salario)

    cursor.execute(query)
    funcionarios = cursor.fetchall()

    conn.close()

    return render_template('lista_funcionarios.html', funcionarios=funcionarios, filtro_codigo=filtro_codigo, filtro_nome=filtro_nome, filtro_data_nascimento=filtro_data_nascimento, filtro_salario=filtro_salario)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_funcionario():
    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        salario = request.form['salario']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO funcionarios (nome, data_nascimento, salario)
            VALUES (?, ?, ?)
        ''', (nome, data_nascimento, salario))

        conn.commit()
        conn.close()

        return redirect('/')
    else:
        return render_template('adicionar_funcionario.html')

@app.route('/editar/<int:funcionario_id>', methods=['GET', 'POST'])
def editar_funcionario(funcionario_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        salario = request.form['salario']

        cursor.execute('''
            UPDATE funcionarios
            SET nome = ?, data_nascimento = ?, salario = ?
            WHERE id = ?
        ''', (nome, data_nascimento, salario, funcionario_id))

        conn.commit()
        conn.close()

        return redirect('/')
    else:
        cursor.execute('SELECT * FROM funcionarios WHERE id = ?', (funcionario_id,))
        funcionario = cursor.fetchone()

        conn.close()

        if funcionario:
            return render_template('editar_funcionario.html', funcionario=funcionario)
        else:
            return 'Funcionário não encontrado.'

@app.route('/remover', methods=['POST'])
def remover_funcionario():
    funcionario_id = request.form['funcionario_id']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM funcionarios WHERE id = ?", (funcionario_id,))
    conn.commit()

    conn.close()

    return redirect('/')

criar_tabela()

if __name__ == '__main__':
    app.run()