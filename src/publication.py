#Importando classes
import src.curriculum as curriculum


class Publication:
	
	#???? Perguntar utilidade para Jean	
	# type_list = ["TCC", "IC"]
	# status_list = ["In Progress", "Concluded"]

	def __init__(self, id=None):
		self.id = id #???? como definir o id para dar match com orintador orientado e participante de banca
		self.title = None
		self.author_name_list = None
		# self.advisor_name = None #??? Precisa?
		self.year = None
		self.country = None
		self.status = None #Concluida ou em andamento
		self.type = None #TCC ou IC
		self.lang = None
		self.name_institution = None
		self.name_course = None
		self.name_cod = None
	
	#Pegando dados das orientações concluidas
	def get_data_advidor_publication(self, root):
		#Navegando por outras produções
		for other_prod in root.findall('.//OUTRA-PRODUCAO'): 
			#Criando lista de orientações concluídas
			other_prod_list = other_prod.findall('.//ORIENTACOES-CONCLUIDAS')
			
			#Navegando na lista de orientações concluídas
			for completed_prod in other_prod_list:
				completed_prod_list = completed_prod.findall('.//OUTRAS-ORIENTACOES-CONCLUIDAS')
				
				#Navegando pelos dados básicos de orientações concluidas
				for completed_prod_item in completed_prod_list:
					data_completed_prod = completed_prod_item.find('.//DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')
					if data_completed_prod is not None:
						#Tornando o status da classe em concluido
						self.status = 'Concluded'
						#Adicionando atributos na classe
						self.title = data_completed_prod.attrib.get('TITULO')
						self.year = data_completed_prod.attrib.get('ANO')
						self.country = data_completed_prod.attrib.get('PAIS')
						self.lang = data_completed_prod.attrib.get('IDIOMA')
						self.type = data_completed_prod.attrib.get('NATUREZA')
						
				#Navegando pelos dados detalhados de orientações concluidas
				for completed_prod_item in completed_prod_list:
					details_completed_prod = completed_prod_item.find('.//DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')
					if details_completed_prod is not None:		
						
						#Adicionando atributos na classe
						self.name_institution = details_completed_prod.attrib.get('NOME-DA-INSTITUICAO')
						self.name_course = details_completed_prod.attrib.get('NOME-DO-CURSO')
						self.cod_course = details_completed_prod.attrib.get('CODIGO-CURSO')
						
						#Extraindo lista de autores do xml
						self.authors_name = details_completed_prod.attrib.get('NOME-DO-ORIENTADO')
						
	#Função que formata impressão de publicações	
	def print_publication(self):
		print("----------------Publicação-----------------")
		# authors_formatted = ', '.join(self.format_authors())
		print(f"ID: {self.id}")
		print(f"Título: {self.title}")
		print(f"Autores: {self.authors_name}")
		# print(f"Orientador: {self.advisor_name}")
		print(f"Ano: {self.year}")
		print(f"País: {self.country}")
		print(f"Status: {self.status}")
		print(f"Tipo: {self.type}")
		print(f"Idioma: {self.lang}")
		print(f"Instituição: {self.name_institution}")
		print(f"Curso: {self.name_course}")
		print(f"Código do Curso: {self.cod_course}")				


	#Ainda não funciona	
	# def format_authors(self):
	# 	formatted_authors = []
		
	# 	authors = self.authors_xml.split(' e')
		
	# 	for author in authors:
			
	# 		if len(author) > 1:
	# 			formatted_authors.append(parts)
	# 		else:
	# 			print("errou")
			
	# 	return formatted_authors

