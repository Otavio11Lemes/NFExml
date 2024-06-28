import xml.etree.ElementTree as ET
import psycopg2

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

# Carregar o arquivo XML
tree = ET.parse('./Xmls/52240602924249000119550020018676171243672280-nfe.xml')
root = tree.getroot()

# Definir o namespace
ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

# Conectar ao banco de dados
conn = connect_db()
cur = conn.cursor()


# Criar as tabelas, se não existirem
cur.execute('''
    CREATE TABLE IF NOT EXISTS emitente (
        cnpj VARCHAR PRIMARY KEY,
        inscricao_estadual VARCHAR,
        razao_social VARCHAR,
        logradouro VARCHAR,
        numero VARCHAR,
        bairro VARCHAR,
        municipio VARCHAR,
        uf VARCHAR
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS imposto (
        id SERIAL PRIMARY KEY,
        aliquota_icms VARCHAR,
        aliquota_icms_st VARCHAR,
        aliquota_ipi VARCHAR
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS produto (
        id SERIAL PRIMARY KEY,
        cean VARCHAR,
        descricao VARCHAR,
        ncm VARCHAR,
        cst VARCHAR,
        cfop VARCHAR,
        unidade VARCHAR,
        quantidade VARCHAR,
        valor_unitario VARCHAR,
        cnpj_emitente VARCHAR,
        data DATE,
        FOREIGN KEY (cnpj_emitente) REFERENCES emitente(cnpj)
    )
''')

# Extrair dados do emitente
emitente = root.find('.//nfe:emit', ns)
CNPJ = emitente.find('nfe:CNPJ', ns).text
inscricao_estadual = emitente.find('nfe:IE', ns).text
razao_social = emitente.find('nfe:xNome', ns).text
logradouro = emitente.find('nfe:enderEmit/nfe:xLgr', ns).text
numero = emitente.find('nfe:enderEmit/nfe:nro', ns).text
bairro = emitente.find('nfe:enderEmit/nfe:xBairro', ns).text
municipio = emitente.find('nfe:enderEmit/nfe:xMun', ns).text
uf = emitente.find('nfe:enderEmit/nfe:UF', ns).text

# Inserir dados do emitente na tabela
cur.execute('''
    INSERT INTO emitente (cnpj, inscricao_estadual, razao_social, logradouro, numero, bairro, municipio, uf)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (cnpj) DO NOTHING
''', (CNPJ, inscricao_estadual, razao_social, logradouro, numero, bairro, municipio, uf))

# Extrair a data do XML
data_emissao = root.find('.//nfe:ide/nfe:dhEmi', ns).text.split('T')[0]  # Assume que a data está no formato "AAAA-MM-DDTHH:MM:SS"

# Extrair dados dos produtos e associar ao emitente
for det in root.findall('.//nfe:det', ns):
    # Produto
    cEAN = det.find('nfe:prod/nfe:cEAN', ns).text
    descricao = det.find('nfe:prod/nfe:xProd', ns).text
    ncm = det.find('nfe:prod/nfe:NCM', ns).text
    cst = det.find('nfe:imposto/nfe:ICMS//nfe:CST', ns).text
    cfop = det.find('nfe:prod/nfe:CFOP', ns).text
    unidade = det.find('nfe:prod/nfe:uCom', ns).text
    quantidade = det.find('nfe:prod/nfe:qCom', ns).text
    valor_unitario = det.find('nfe:prod/nfe:vUnCom', ns).text

    # Inserir dados do produto na tabela, associando ao emitente
    cur.execute('''
        INSERT INTO produto (cean, descricao, ncm, cst, cfop, unidade, quantidade, valor_unitario, cnpj_emitente, data)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (cEAN, descricao, ncm, cst, cfop, unidade, quantidade, valor_unitario, CNPJ, data_emissao))

    # Impostos
    aliquota_ICMS = det.find('nfe:imposto/nfe:ICMS//nfe:pICMS', ns)
    aliquota_ICMS_ST = det.find('nfe:imposto/nfe:ICMS//nfe:pICMSST', ns)
    aliquota_IPI = det.find('nfe:imposto/nfe:IPI//nfe:pIPI', ns)

    # Verificar se os elementos são None antes de acessar o atributo text
    aliquota_ICMS = aliquota_ICMS.text if aliquota_ICMS is not None else None
    aliquota_ICMS_ST = aliquota_ICMS_ST.text if aliquota_ICMS_ST is not None else None
    aliquota_IPI = aliquota_IPI.text if aliquota_IPI is not None else None

    # Inserir dados do imposto na tabela (opcional, depende da estrutura do seu banco)
    cur.execute('''
        INSERT INTO imposto (aliquota_icms, aliquota_icms_st, aliquota_ipi)
        VALUES (%s, %s, %s)
    ''', (aliquota_ICMS, aliquota_ICMS_ST, aliquota_IPI))

# Confirmar transações e fechar conexão
conn.commit()
cur.close()
conn.close()
