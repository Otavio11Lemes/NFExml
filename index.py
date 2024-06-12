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
headers_nfe = ["cUF", "cNF", "natOp"]  # Adicione mais cabeçalhos conforme necessário
headers_prot = ["nProt", "dhRecbto", "cStat", "xMotivo"]  # Adicione mais cabeçalhos conforme necessário

# Preencher o cabeçalho na primeira linha
ws.append(headers_nfe + headers_prot)

# Extrair dados da NF-e
infNFe = root.find('.//nfe:NFe/nfe:infNFe', ns)
cUF = infNFe.find('nfe:ide/nfe:cUF', ns).text
cNF = infNFe.find('nfe:ide/nfe:cNF', ns).text
natOp = infNFe.find('nfe:ide/nfe:natOp', ns).text

# Extrair dados do protocolo
protNFe = root.find('.//nfe:protNFe', ns)
nProt = protNFe.find('nfe:infProt/nfe:nProt', ns).text
dhRecbto = protNFe.find('nfe:infProt/nfe:dhRecbto', ns).text
cStat = protNFe.find('nfe:infProt/nfe:cStat', ns).text
xMotivo = protNFe.find('nfe:infProt/nfe:xMotivo', ns).text

# Adicionar os dados à próxima linha
ws.append([cUF, cNF, natOp, nProt, dhRecbto, cStat, xMotivo])

# Salvar o arquivo
wb.save("dados_nfe.xlsx")
