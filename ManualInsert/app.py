from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

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

@app.route('/add', methods=['POST'])
def add_data():
    if request.method == 'POST':
        try:
            # Emitente
            cnpj = request.form.get('cnpj')
            inscricao_estadual = request.form.get('inscricao_estadual')
            razao_social = request.form.get('razao_social')
            logradouro = request.form.get('logradouro')
            numero = request.form.get('numero')
            bairro = request.form.get('bairro')
            municipio = request.form.get('municipio')
            uf = request.form.get('uf')
            
            # Produto
            cean = request.form.get('cean')
            descricao = request.form.get('descricao')
            ncm = request.form.get('ncm')
            cst = request.form.get('cst')
            cfop = request.form.get('cfop')
            unidade = request.form.get('unidade')
            quantidade = request.form.get('quantidade')
            valor_unitario = request.form.get('valor_unitario')
            data = request.form.get('data')
            
            # Imposto
            aliquota_icms = request.form.get('aliquota_icms')
            aliquota_icms_st = request.form.get('aliquota_icms_st')
            aliquota_ipi = request.form.get('aliquota_ipi')

            conn = connect_db()
            cur = conn.cursor()

            # Verificar se cnpj não é nulo antes de inserir emitente
            if cnpj:
                cur.execute('''
                    INSERT INTO emitente (cnpj, inscricao_estadual, razao_social, logradouro, numero, bairro, municipio, uf)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (cnpj) DO NOTHING
                ''', (cnpj, inscricao_estadual, razao_social, logradouro, numero, bairro, municipio, uf))

            # Verificar se cean não é nulo antes de inserir produto
            if cean:
                cur.execute('''
                    INSERT INTO produto (cean, descricao, ncm, cst, cfop, unidade, quantidade, valor_unitario, cnpj_emitente, data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (cean, descricao, ncm, cst, cfop, unidade, quantidade, valor_unitario, cnpj, data))

            # Inserir dados do imposto na tabela (opcional)
            cur.execute('''
                INSERT INTO imposto (aliquota_icms, aliquota_icms_st, aliquota_ipi)
                VALUES (%s, %s, %s)
            ''', (aliquota_icms, aliquota_icms_st, aliquota_ipi))

            conn.commit()
            cur.close()
            conn.close()

            return redirect(url_for('index'))
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return "Erro ao adicionar dados."

if __name__ == '__main__':
    app.run(debug=True)
