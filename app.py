from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

DB_NAME = "database.db"


def conectar_banco():
    conexao = sqlite3.connect(DB_NAME)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessoes_estudo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            materia_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            duracao INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (materia_id) REFERENCES materias(id)
        )
    """)

    conexao.commit()
    conexao.close()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM materias")
    total_materias = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM sessoes_estudo")
    total_sessoes = cursor.fetchone()["total"]

    cursor.execute("SELECT COALESCE(SUM(duracao), 0) AS total FROM sessoes_estudo")
    total_minutos = cursor.fetchone()["total"]

    total_horas = round(total_minutos / 60, 2)

    meta_semanal_minutos = 600

    if meta_semanal_minutos > 0:
        progresso_percentual = round((total_minutos / meta_semanal_minutos) * 100)
    else:
        progresso_percentual = 0

    if progresso_percentual > 100:
        progresso_percentual = 100

    if total_horas == 0:
        nivel = "Iniciante"
        mensagem = "Comece registrando sua primeira sessão de estudo."
    elif total_horas < 3:
        nivel = "Estudante em construção"
        mensagem = "Bom começo. Continue alimentando seu histórico de estudos."
    elif total_horas < 10:
        nivel = "Estudante focado"
        mensagem = "Você está no caminho certo. Continue mantendo a constância."
    else:
        nivel = "Estudante disciplinado"
        mensagem = "Excelente ritmo. Seu desempenho mostra consistência nos estudos."

    cursor.execute("""
        SELECT 
            sessoes_estudo.id,
            materias.nome AS materia,
            sessoes_estudo.descricao,
            sessoes_estudo.duracao,
            sessoes_estudo.data
        FROM sessoes_estudo
        INNER JOIN materias ON materias.id = sessoes_estudo.materia_id
        ORDER BY sessoes_estudo.id DESC
        LIMIT 5
    """)

    ultimas_sessoes = cursor.fetchall()

    conexao.close()

    return render_template(
        "dashboard.html",
        total_materias=total_materias,
        total_sessoes=total_sessoes,
        total_minutos=total_minutos,
        total_horas=total_horas,
        meta_semanal_minutos=meta_semanal_minutos,
        progresso_percentual=progresso_percentual,
        nivel=nivel,
        mensagem=mensagem,
        ultimas_sessoes=ultimas_sessoes
    )


@app.route("/materias", methods=["GET", "POST"])
def materias():
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]

        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO materias (nome, descricao)
            VALUES (?, ?)
        """, (nome, descricao))

        conexao.commit()
        conexao.close()

        return redirect(url_for("materias"))

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM materias ORDER BY id DESC")
    lista_materias = cursor.fetchall()

    conexao.close()

    return render_template("materias.html", materias=lista_materias)

@app.route("/materias/editar/<int:id>", methods=["GET", "POST"])
def editar_materia(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]

        cursor.execute("""
            UPDATE materias
            SET nome = ?, descricao = ?
            WHERE id = ?
        """, (nome, descricao, id))

        conexao.commit()
        conexao.close()

        return redirect(url_for("materias"))

    cursor.execute("SELECT * FROM materias WHERE id = ?", (id,))
    materia = cursor.fetchone()

    conexao.close()

    if materia is None:
        return redirect(url_for("materias"))

    return render_template("editar_materia.html", materia=materia)

@app.route("/materias/excluir/<int:id>", methods=["POST"])
def excluir_materia(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM sessoes_estudo WHERE materia_id = ?", (id,))
    cursor.execute("DELETE FROM materias WHERE id = ?", (id,))

    conexao.commit()
    conexao.close()

    return redirect(url_for("materias"))

@app.route("/sessoes", methods=["GET", "POST"])
def sessoes():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    if request.method == "POST":
        materia_id = request.form["materia_id"]
        descricao = request.form["descricao"]
        duracao = request.form["duracao"]
        data_estudo = request.form["data"]

        cursor.execute("""
            INSERT INTO sessoes_estudo (materia_id, descricao, duracao, data)
            VALUES (?, ?, ?, ?)
        """, (materia_id, descricao, duracao, data_estudo))

        conexao.commit()
        conexao.close()

        return redirect(url_for("sessoes"))

    cursor.execute("SELECT * FROM materias ORDER BY nome ASC")
    lista_materias = cursor.fetchall()

    cursor.execute("""
        SELECT 
            sessoes_estudo.id,
            materias.nome AS materia,
            sessoes_estudo.descricao,
            sessoes_estudo.duracao,
            sessoes_estudo.data
        FROM sessoes_estudo
        INNER JOIN materias ON materias.id = sessoes_estudo.materia_id
        ORDER BY sessoes_estudo.id DESC
    """)
    lista_sessoes = cursor.fetchall()

    conexao.close()

    data_atual = date.today().isoformat()

    return render_template(
        "sessoes.html",
        materias=lista_materias,
        sessoes=lista_sessoes,
        data_atual=data_atual
    )

@app.route("/sessoes/editar/<int:id>", methods=["GET", "POST"])
def editar_sessao(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    if request.method == "POST":
        materia_id = request.form["materia_id"]
        descricao = request.form["descricao"]
        duracao = request.form["duracao"]
        data_estudo = request.form["data"]

        cursor.execute("""
            UPDATE sessoes_estudo
            SET materia_id = ?, descricao = ?, duracao = ?, data = ?
            WHERE id = ?
        """, (materia_id, descricao, duracao, data_estudo, id))

        conexao.commit()
        conexao.close()

        return redirect(url_for("sessoes"))

    cursor.execute("SELECT * FROM sessoes_estudo WHERE id = ?", (id,))
    sessao = cursor.fetchone()

    cursor.execute("SELECT * FROM materias ORDER BY nome ASC")
    materias = cursor.fetchall()

    conexao.close()

    if sessao is None:
        return redirect(url_for("sessoes"))

    return render_template(
        "editar_sessao.html",
        sessao=sessao,
        materias=materias
    )

@app.route("/sessoes/excluir/<int:id>", methods=["POST"])
def excluir_sessao(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM sessoes_estudo WHERE id = ?", (id,))

    conexao.commit()
    conexao.close()

    return redirect(url_for("sessoes"))

if __name__ == "__main__":
    criar_tabelas()
    app.run(debug=True)