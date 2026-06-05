from flask import Flask, render_template, request, redirect, url_for
import sqlite3

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


if __name__ == "__main__":
    criar_tabelas()
    app.run(debug=True)