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
headers_nfe = ["cEAN", "xProd", "NCM", "CEST", "CFOP", "uCom", "qCom", "vUnCom", "pPIS", "pICMS", "pIPI", "pCOFINS"]  # cabeçalho produto

# Preencher o cabeçalho na primeira linha
ws.append(headers_prot + headers_nfe)

# Função auxiliar para obter o texto de um elemento XML
def get_text_or_none(element, path, ns):
    found = element.find(path, ns)
    return found.text if found is not None else ''

# Extrair dados do emitente
emit = root.find('.//nfe:emit', ns)
CNPJ = get_text_or_none(emit, 'nfe:CNPJ', ns)
fone = get_text_or_none(emit, 'nfe:enderEmit/nfe:fone', ns)
xNome = get_text_or_none(emit, 'nfe:xNome', ns)

# Extrair dados dos produtos (det)
for det in root.findall('.//nfe:det', ns):
    cEAN = get_text_or_none(det, './/nfe:cEAN', ns)
    xProd = get_text_or_none(det, './/nfe:xProd', ns)
    NCM = get_text_or_none(det, './/nfe:NCM', ns)
    CEST = get_text_or_none(det, './/nfe:CEST', ns)
    CFOP = get_text_or_none(det, './/nfe:CFOP', ns)
    uCom = get_text_or_none(det, './/nfe:uCom', ns)
    qCom = get_text_or_none(det, './/nfe:qCom', ns)
    vUnCom = get_text_or_none(det, './/nfe:vUnCom', ns)
    pPIS = get_text_or_none(det, './/nfe:PIS//nfe:pPIS', ns)
    pICMS = get_text_or_none(det, './/nfe:ICMS//nfe:pICMS', ns)
    pIPI = get_text_or_none(det, './/nfe:IPI//nfe:pIPI', ns)
    pCOFINS = get_text_or_none(det, './/nfe:COFINS//nfe:pCOFINS', ns)

    # Adicionar os dados à próxima linha
    ws.append([CNPJ, fone, xNome, cEAN, xProd, NCM, CEST, CFOP, uCom, qCom, vUnCom, pPIS, pICMS, pIPI, pCOFINS])

# Salvar o arquivo
wb.save("dados_nfe.xlsx")
