#Importando classes
import xml.etree.ElementTree as ET

class Pesquisador:
	
	def __init__(self):
		self.nome = ""
		self.id_lattes = ""
		self.nacionalidade = ""
		self.data_atualizacao = ""
		self.role = ""
		
	def get_data(self, root):

		# If an ElementTree object was passed, get its root element
		if isinstance(root, ET.ElementTree):
			root = root.getroot()

		# CURRICULO-VITAE may be the root or a child; find it first
		cv = None
		if root.tag == 'CURRICULO-VITAE':
			cv = root
		else:
			cv = root.find('CURRICULO-VITAE')

		if cv is not None:
			# attributes on CURRICULO-VITAE
			data = cv.get('DATA-ATUALIZACAO', '')
			normalized_date = self.normalize_date(data)
			self.data_atualizacao =  normalized_date or self.data_atualizacao
			self.id_lattes = cv.get('NUMERO-IDENTIFICADOR', '') or self.id_lattes

		# DADOS-GERAIS may be a direct child of CURRICULO-VITAE or appear elsewhere; try both
		dados = None
		if cv is not None:
			dados = cv.find('DADOS-GERAIS')
		if dados is None:
			dados = root.find('.//DADOS-GERAIS')

		if dados is not None:
			# Normalize to the attributes the XML uses
			self.nome = dados.get('NOME-COMPLETO', '')
			# There are a few different attribute names sometimes used; try common variants
			self.nacionalidade = (
				dados.get('PAIS-DE-NACIONALIDADE') or
				dados.get('PAIS-DE-NASCIMENTO') or
				dados.get('NACIONALIDADE') or
				''
			)
		# Busca por bancas no curriculo
		part_banca = None
		if cv is not None:
			part_banca = cv.find('.//PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO')
			self.role = 'Avaliador'
		if part_banca is None:
			part_banca = root.find('.//PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO')
			self.role = 'Orientando'

		return
	
	def normalize_date(self, data):
		if not data:
			return None
		s = str(data).strip()
		# DDMMYYYY -> YYYY-MM-DD
		if len(s) == 8 and s.isdigit():
			return f"{s[4:8]}-{s[2:4]}-{s[0:2]}"
		# se já estiver em ISO ou outro formato, retorna o valor limpo
		return s
		

		
	