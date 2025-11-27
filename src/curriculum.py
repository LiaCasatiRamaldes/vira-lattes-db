class Curriculum:	
	
	# date_str = None

	def __init__(self):
		self.name = None
		self.last_att = None
		self.lattes_id = None
		self.nacionality = None
		
		self.publications = {} #Dicionario de publicações
		self.adivisor_publications = {} #Lista de publicações como orientador

	#Função extrai do xml e adiciona na classe curriculum
	def get_data(self, root):
		#Navegando por curriculo e pegando dados do curriculo
		for cv_data in root.iter('CURRICULO-VITAE'):
			date_str = cv_data.get('DATA-ATUALIZACAO')
			self.lattes_id = cv_data.get('NUMERO-IDENTIFICADOR')
		#Formatando a data antes de adicionar no atributo data de atualização	
		self.last_att = self.format_date(date_str)	
		
		#Navegando por dados gerais e pegando dados do pesquisador no curriculo	
		for general_data in root.iter('DADOS-GERAIS'):
			self.name = general_data.get('NOME-COMPLETO')
			self.nacionality = general_data.get('PAIS-DE-NACIONALIDADE')
	
	
	#Função que formata impressão de dados do curriculo
	def print_curriculum(self):
		print("----------------Curriculum-----------------")
		
		print(f"Nome: {self.name}")
		print(f"Última Atualização: {self.last_att}")
		print(f"ID Lattes: {self.lattes_id}")
		print(f"Nacionalidade: {self.nacionality}")
		
		print("\nPublicações:")
		for pub_id, pub in self.publications.items():
			print(f"  ID: {pub_id}, Título: {pub.title}, Ano: {pub.year}")
		
		print("\nPublicações como Orientador:")
		for pub_id, pub in self.adivisor_publications.items():
			print(f"  ID: {pub_id}, Título: {pub.title}, Ano: {pub.year}")
			
	#Função para formatar a data		
	def format_date(self, date_str):
		if len(date_str) == 8:
			day = date_str[:2]
			month = date_str[2:4]
			year = date_str[4:]
			return f"{day}/{month}/{year}" 
		else:
			return "Data inválida" 
		
	