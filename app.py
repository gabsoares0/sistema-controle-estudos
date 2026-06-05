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


if __name__ == "__main__":
    criar_tabelas()
    app.run(debug=True)