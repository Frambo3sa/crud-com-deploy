

from flask import Flask, render_template, redirect, request, flash
import mysql.connector
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FRANCPAES'
logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/m')
def home_medico():
    global logado
    logado = False
    return render_template('cadastrodemed.html')

@app.route('/consulta')
def home_consultas():
    global logado
    logado = False
    return render_template('marcar_consulta.html')

@app.route('/adm')
def adm():
    if logado:
        conectBD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='admin')
        if conectBD.is_connected():
            cursur = conectBD.cursor()
            cursur.execute('SELECT * FROM usuario;')
            usuarios = cursur.fetchall()
            cursur.close()
            conectBD.close()
        return render_template("administrador.html", usuarios=usuarios)
    else:
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='admin')
    if conectBD.is_connected():
        cursur = conectBD.cursor()
        cursur.execute('SELECT * FROM usuario;')
        usuariosBD = cursur.fetchall()
        for usuario in usuariosBD:
            if nome == 'adm' and senha == '000':
                logado = True
                return redirect('/adm')
            if usuario[1] == nome and usuario[2] == senha:
                return render_template("usuarios.html")
        flash('USUARIO INVALIDO')
    conectBD.close()
    return redirect("/")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='admin')
    if conectBD.is_connected():
        cursur = conectBD.cursor()
        cursur.execute(f"INSERT INTO usuario (nome, senha) VALUES ('{nome}', '{senha}');")
        conectBD.commit()
        cursur.close()
        conectBD.close()
    flash(f'{nome} CADASTRADO!!')
    return redirect('/adm')

@app.route('/consultarUsuario', methods=['POST'])
def consultarUsuario():
    nome = request.form.get('nome')
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='admin')
    if conectBD.is_connected():
        cursur = conectBD.cursor()
        cursur.execute(f"SELECT * FROM usuario WHERE nome = '{nome}';")
        usuario = cursur.fetchone()
        cursur.close()
        conectBD.close()
        if usuario:
            return f"Usuário encontrado: ID={usuario[0]}, Nome={usuario[1]}, Senha={usuario[2]}"
        else:
            flash('USUARIO NÃO ENCONTRADO')
    return redirect('/adm')

@app.route('/alterarUsuario', methods=['POST'])
def alterarUsuario():
    usuarioID = request.form.get('usuarioPalterar')
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='admin')
    if conectBD.is_connected():
        cursur = conectBD.cursor()
        cursur.execute(f"UPDATE usuario SET nome = '{nome}', senha = '{senha}' WHERE id = '{usuarioID}';")
        conectBD.commit()
        cursur.close()
        conectBD.close()
    flash(f'Usuário ID={usuarioID} ALTERADO')
    return redirect('/adm')

@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    usuarioID = request.form.get('usuarioPexcluir')
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='admin')
    if conectBD.is_connected():
        cursur = conectBD.cursor()
        cursur.execute(f"DELETE FROM usuario WHERE id = '{usuarioID}';")
        conectBD.commit()
        cursur.close()
        conectBD.close()
    flash(f'Usuário ID={usuarioID} EXCLUIDO')
    return redirect('/adm')

# Rotas para médicos (cadastrar, consultar, alterar, excluir)
@app.route('/cadastrarMedico', methods=['POST'])
def cadastrarMedico():
    nome = request.form.get('nomeM')
    senha = request.form.get('senhaM')
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='admin')
    if conectBD.is_connected():
        cursur = conectBD.cursor()
        cursur.execute(f"INSERT INTO medico (nomem, senham) VALUES ('{nome}', '{senha}');")
        conectBD.commit()
        cursur.close()
        conectBD.close()
    flash(f'{nome} CADASTRADO!!')
    return redirect('/m')

@app.route('/consultarMedico', methods=['POST'])
def consultarMedico():
    nome = request.form.get('nomeM')
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='admin')
    if conectBD.is_connected():
        cursur = conectBD.cursor()
        cursur.execute(f"SELECT * FROM medico WHERE nomem = '{nome}';")
        medico = cursur.fetchone()
        cursur.close()
        conectBD.close()
        if medico:
            return f"Médico encontrado: ID={medico[0]}, Nome={medico[1]}, Senha={medico[2]}"
        else:
            flash('MÉDICO NÃO ENCONTRADO')
    return redirect('/m')

@app.route('/alterarMedico', methods=['POST'])
def alterarMedico():
    medicoID = request.form.get('medicoPalterar')
    nome = request.form.get('nomeM')
    senha = request.form.get('senhaM')
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='admin')
    if conectBD.is_connected():
        cursur = conectBD.cursor()
        cursur.execute(f"UPDATE medico SET nomem = '{nome}', senham = '{senha}' WHERE idm = '{medicoID}';")
        conectBD.commit()
        cursur.close()
        conectBD.close()
    flash(f'Médico ID={medicoID} ALTERADO')
    return redirect('/m')

@app.route('/excluirMedico', methods=['POST'])
def excluirMedico():
    medicoID = request.form.get('medicoPexcluir')
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='admin')
    if conectBD.is_connected():
        cursur = conectBD.cursor()
        cursur.execute(f"DELETE FROM medico WHERE idm = '{medicoID}';")
        conectBD.commit()
        cursur.close()
        conectBD.close()
    flash(f'Médico ID={medicoID} EXCLUIDO')
    return redirect('/m')


@app.route('/marcarConsulta', methods=['POST'])
def marcarConsulta():
    idu = request.form.get('idu')
    idme = request.form.get('idme')
    descricao = request.form.get('descricao')
    
    conectBD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='admin')
    
    if conectBD.is_connected():
        cursur = conectBD.cursor()
        cursur.execute(f"INSERT INTO consulta (idu, idme, descricao) VALUES ('{idu}', '{idme}', '{descricao}');")
        conectBD.commit()
        cursur.close()
        conectBD.close()
    
    flash(f'Consulta marcada com sucesso!')
    return redirect('/m')


@app.route("/upload", methods=['POST'])
def upload():
    global logado
    logado = True
    arquivo = request.files.get('documento')
    nome_arquivo = arquivo.filename.replace(" ", "-")
    arquivo.save(os.path.join('../001/static/css/arquivos/', nome_arquivo))
    flash('Arquivo salvo')
    return redirect('/adm')

if __name__ == "__main__":
    app.run(debug=True)
