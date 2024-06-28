from flask import Flask, request, jsonify
import psycopg2  # Você precisará instalar psycopg2 se estiver usando PostgreSQL

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'database': 'mercadomoviments',
    'user': 'postgres',
    'password': '70207811'
}

# Função para inserir dados no banco de dados
def inserir_dados_emitente(cnpj, inscricao_estadual, razao_social, logradouro, numero, bairro, municipio, uf):
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO emitente (cnpj, inscricao_estadual, razao_social, logradouro, numero, bairro, municipio, uf)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (cnpj, inscricao_estadual, razao_social, logradouro, numero, bairro, municipio, uf))
        connection.commit()
        return True
    except Exception as e:
        print(f"Erro ao inserir dados no banco de dados: {str(e)}")
        return False
    finally:
        cursor.close()
        connection.close()

@app.route('/inserir_emitente', methods=['POST'])
def inserir_emitente():
    data = request.json
    sucesso = inserir_dados_emitente(data['cnpj'], data['inscricao_estadual'], data['razao_social'],
                                    data['logradouro'], data['numero'], data['bairro'], data['municipio'], data['uf'])
    if sucesso:
        return jsonify({'status': 'sucesso', 'mensagem': 'Dados inseridos com sucesso!'}), 201
    else:
        return jsonify({'status': 'erro', 'mensagem': 'Erro ao inserir dados no banco de dados!'}), 500

if __name__ == '__main__':
    app.run(debug=True)
