import xml.etree.ElementTree as ET
from openpyxl import Workbook

# Carregar o arquivo XML
tree = ET.parse('./Xmls/52240602924249000119550020018676171243672280-nfe.xml')
root = tree.getroot()

# Definir o namespace
ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

# Criar um novo arquivo XLSX
wb = Workbook()
ws = wb.active

# Definir os cabeçalhos
headers_prot = ["CNPJ", "fone", "xNome"]  # cabeçalho remetente
headers_nfe = ["cEAN", "xProd", "NCM", "CEST", "CFOP", "uCom", "qCom", "vUnCom", "pPIS", "pICMS", "pIPI",  "pCOFINS"]  # cabeçalho produto

# Preencher o cabeçalho na primeira linha
ws.append(headers_nfe + headers_prot)

# Extrair dados da NF-e
infNFe = root.find('.//nfe:NFe/nfe:infNFe', ns)
if infNFe is not None:
    cUF = infNFe.find('nfe:ide/nfe:cUF', ns).text if infNFe.find('nfe:ide/nfe:cUF', ns) is not None else ''
    cNF = infNFe.find('nfe:ide/nfe:cNF', ns).text if infNFe.find('nfe:ide/nfe:cNF', ns) is not None else ''
    natOp = infNFe.find('nfe:ide/nfe:natOp', ns).text if infNFe.find('nfe:ide/nfe:natOp', ns) is not None else ''
else:
    cUF, cNF, natOp = '', '', ''

# Extrair dados do protocolo
protNFe = root.find('.//nfe:protNFe', ns)
if protNFe is not None:
    nProt = protNFe.find('nfe:infProt/nfe:nProt', ns).text if protNFe.find('nfe:infProt/nfe:nProt', ns) is not None else ''
    dhRecbto = protNFe.find('nfe:infProt/nfe:dhRecbto', ns).text if protNFe.find('nfe:infProt/nfe:dhRecbto', ns) is not None else ''
    cStat = protNFe.find('nfe:infProt/nfe:cStat', ns).text if protNFe.find('nfe:infProt/nfe:cStat', ns) is not None else ''
    xMotivo = protNFe.find('nfe:infProt/nfe:xMotivo', ns).text if protNFe.find('nfe:infProt/nfe:xMotivo', ns) is not None else ''
else:
    nProt, dhRecbto, cStat, xMotivo = '', '', '', ''

# Extrair o nome do emitente (xNome) dentro do elemento emit
emit = infNFe.find('nfe:emit', ns)
if emit is not None:
    xNome = emit.find('nfe:xNome', ns).text if emit.find('nfe:xNome', ns) is not None else ''
else:
    xNome = ''

# Adicionar os dados à próxima linha
ws.append([cUF, cNF, natOp, nProt, dhRecbto, cStat, xMotivo, xNome])

# Salvar o arquivo
wb.save("dados_nfe.xlsx")
