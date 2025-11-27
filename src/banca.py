import xml.etree.ElementTree as ET

class Banca:
	
	def __init__(self, id_banca=0, ano_banca='', idioma='', natureza='', titulo=''):
		self.id_banca = id_banca
		self.ano_banca = ano_banca
		self.idioma = idioma
		self.natureza = natureza
		self.titulo = titulo
		self.banca_list = []
		
	def get_data(self, root):

		if isinstance(root, ET.ElementTree):
			root = root.getroot()
			
		cv = None
		if root.tag == 'CURRICULO-VITAE':
			cv = root
		else:
			cv = root.find('CURRICULO-VITAE')

		# Busca por bancas no curriculo
		part_banca = None
		if cv is not None:
			part_banca = cv.find('.//PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO')
		if part_banca is None:
			part_banca = root.find('.//PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO')

		# iterar sobre cada banca encontrada
		if part_banca is not None:
			for banca_el in part_banca.findall('PARTICIPACAO-EM-BANCA-DE-GRADUACAO'):
				# seq = banca_el.get('SEQUENCIA-PRODUCAO', '').strip()
				self.id_banca += 1
				dados = banca_el.find('DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-GRADUACAO')
				if dados is not None:
					ano = dados.get('ANO', '').strip()
					idioma = dados.get('IDIOMA', '').strip()
					natureza = dados.get('NATUREZA', '').strip()
				else:
					ano = ''
					idioma = ''
					natureza = ''

				item = {
					'id_banca': str(self.id_banca),
					'ano_banca': ano,
					'idioma': idioma,
					'natureza': natureza
				}
				self.banca_list.append(item)
		# Se houver apenas uma banca, populate os atributos da classe também
		if self.banca_list:
			first = self.banca_list[0]
			self.id_banca = first['id_banca']
			self.ano_banca = first['ano_banca']
			self.idioma = first['idioma']
			self.natureza = first['natureza']

		return self.banca_list
