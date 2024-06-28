from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Configurações do banco de dados
DB_HOST = "localhost"
DB_NAME = "nfexml"
DB_USER = "postgres"
DB_PASS = "70207811"

# Função para conectar ao banco de dados
def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        flash('File successfully uploaded')
        return redirect(url_for('map_columns', filename=file.filename))

@app.route('/map_columns/<filename>', methods=['GET', 'POST'])
def map_columns(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_excel(filepath)

    if request.method == 'POST':
        col_mapping = request.form.to_dict()
        insert_data(df, col_mapping)
        flash('Data successfully inserted into the database')
        return redirect(url_for('index'))

    return render_template('map_columns.html', columns=df.columns, filename=filename)

def insert_data(df, col_mapping):
    conn = connect_db()
    cur = conn.cursor()

    for index, row in df.iterrows():
        emitente_data = (
            row.get(col_mapping.get('cnpj')),
            row.get(col_mapping.get('inscricao_estadual')),
            row.get(col_mapping.get('razao_social')),
            row.get(col_mapping.get('logradouro')),
            row.get(col_mapping.get('numero')),
            row.get(col_mapping.get('bairro')),
            row.get(col_mapping.get('municipio')),
            row.get(col_mapping.get('uf'))
        )

        produto_data = (
            row.get(col_mapping.get('cean')),
            row.get(col_mapping.get('descricao')),
            row.get(col_mapping.get('ncm')),
            row.get(col_mapping.get('cst')),
            row.get(col_mapping.get('cfop')),
            row.get(col_mapping.get('unidade')),
            row.get(col_mapping.get('quantidade')),
            row.get(col_mapping.get('valor_unitario')),
            row.get(col_mapping.get('cnpj')),
            row.get(col_mapping.get('data')) if pd.notna(row.get(col_mapping.get('data'))) else None
        )

        imposto_data = (
            row.get(col_mapping.get('aliquota_icms')),
            row.get(col_mapping.get('aliquota_icms_st')),
            row.get(col_mapping.get('aliquota_ipi'))
        )

        if emitente_data[0]:
            cur.execute('''
                INSERT INTO emitente (cnpj, inscricao_estadual, razao_social, logradouro, numero, bairro, municipio, uf)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (cnpj) DO NOTHING
            ''', emitente_data)

        if produto_data[0]:
            cur.execute('''
                INSERT INTO produto (cean, descricao, ncm, cst, cfop, unidade, quantidade, valor_unitario, cnpj_emitente, data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', produto_data)

        cur.execute('''
            INSERT INTO imposto (aliquota_icms, aliquota_icms_st, aliquota_ipi)
            VALUES (%s, %s, %s)
        ''', imposto_data)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
