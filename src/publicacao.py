#Importando classes
import xml.etree.ElementTree as ET

class Publicacao:
	
# <GRADUACAO 00" NOME-CURSO="Sistemas de Informa��o" CODIGO-AREA-CURSO="90000000" STATUS-DO-CURSO="CONCLUIDO" ANO-DE-INICIO="2010" ANO-DE-CONCLUSAO="2016" FLAG-BOLSA="SIM" CODIGO-AGENCIA-FINANCIADORA="045000000000" NOME-AGENCIA="Coordena��o de Aperfei�oamento de Pessoal de N�vel Superior" NUMERO-ID-ORIENTADOR="" CODIGO-CURSO-CAPES="" TITULO-DO-TRABALHO-DE-CONCLUSAO-DE-CURSO-INGLES="" NOME-CURSO-INGLES="" FORMACAO-ACADEMICA-TITULACAO="" TIPO-GRADUACAO="N" CODIGO-INSTITUICAO-GRAD="" NOME-INSTITUICAO-GRAD="" CODIGO-INSTITUICAO-OUTRA-GRAD="" NOME-INSTITUICAO-OUTRA-GRAD="" NOME-ORIENTADOR-GRAD=""/>

	
	def __init__(self, id=0, titulo="", ano_publicacao="", orientador="", id_orientador="", cod_curso="", cod_instituicao="", nome_curso="", nome_instituicao=""):
		self.id = id
		self.titulo = titulo
		self.ano_publicacao = ano_publicacao
		self.orientador = orientador
		self.id_orientador = id_orientador
		self.cod_curso = cod_curso
		self.cod_instituicao = cod_instituicao
		self.nome_curso = nome_curso
		self.nome_instituicao = nome_instituicao
		self.publicacao_list = []
		
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

		# GRADUACAO may be a direct child of CURRICULO-VITAE or appear elsewhere; try both
		formacao = None
		if cv is not None:
			formacao = cv.find('FORMACAO-ACADEMICA-TITULACAO')
		if formacao is None:
			formacao = root.find('.//FORMACAO-ACADEMICA-TITULACAO')

		if formacao is not None:
			for graducao in formacao.findall('GRADUACAO'):
				self.id += 1
				titulo = graducao.get('TITULO-DO-TRABALHO-DE-CONCLUSAO-DE-CURSO', '')
				orientador = graducao.get('NOME-DO-ORIENTADOR', '')
				id_orientador = graducao.get('NUMERO-ID-ORIENTADOR', '')
				cod_curso = graducao.get('CODIGO-CURSO', '')
				cod_instituicao = graducao.get('CODIGO-INSTITUICAO', '')
				nome_curso = graducao.get('NOME-CURSO', '')
				nome_instituicao = graducao.get('NOME-INSTITUICAO', '')
				ano_publicacao = graducao.get('ANO-DE-CONCLUSAO', '')
				
				item = {
					'id': 'pub' + str(self.id),
					'titulo': titulo,
					'orientador': orientador,
					'id_orientador': id_orientador, 
					'cod_curso': cod_curso,
					'cod_instituicao': cod_instituicao,
					'nome_curso': nome_curso,
					'nome_instituicao': nome_instituicao,
					'ano_publicacao': ano_publicacao
				}
				self.publicacao_list.append(item)
				
		# Se houver apenas uma publicação, populate os atributos da classe também
		if self.publicacao_list:
			first = self.publicacao_list[0]
			self.id = first['id']
			self.titulo = first['titulo']
			self.orientador = first['orientador']
			self.id_orientador = first['id_orientador']
			self.cod_curso = first['cod_curso']
			self.cod_instituicao = first['cod_instituicao']
			self.nome_curso = first['nome_curso']
			self.nome_instituicao = first['nome_instituicao']
			self.ano_publicacao = first['ano_publicacao']

		return self.publicacao_list
	

		
	