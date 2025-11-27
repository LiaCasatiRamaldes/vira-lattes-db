#Importando outras classes
# import src.publication as publication
# import src.curriculum as curriculum
import src.publicacao as publicacaoModule
import src.pesquisador as pesquisadorModule
import src.banca as BancaModule
# #Importando libs
import xml.etree.ElementTree as ET
import rdflib
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, OWL

def add_pesquisador(g, pesquisador_obj, pesquisador_uri):
	# pesquisador_uri = URIRef(VIRA_LATTES['Pesquisador'] + '/' + pesquisador_obj.id_lattes)
	g.add((pesquisador_uri, RDF.type, URIRef(VIRA_LATTES['Pesquisador'])))
	g.add((pesquisador_uri, VIRA_LATTES.nome_pesquisador, Literal(pesquisador_obj.nome, lang="pt")))
	g.add((pesquisador_uri, VIRA_LATTES.id_lattes, Literal(pesquisador_obj.id_lattes)))
	g.add((pesquisador_uri, VIRA_LATTES.nacionalidade, Literal(pesquisador_obj.nacionalidade, lang="pt")))
	g.add((pesquisador_uri, VIRA_LATTES.atualizacao, Literal(pesquisador_obj.data_atualizacao)))
	
	pass 

def add_bancas(g, banca_list, pesquisador_uri):
	# Adicionando role do pesquisador e relação com banca ao grafo
	if pesquisador_obj.role == 'Avaliador':
		g.add((pesquisador_uri, RDF.type, URIRef(VIRA_LATTES['Avaliador'])))
		# Iterando sobre as bancas e adicionando ao grafo
		for banca_dict in banca_list:
			banca_uri = URIRef(VIRA_LATTES['Banca'] + '/' +banca_dict['id_banca'])  # URI da banca
			g.add((banca_uri, RDF.type, URIRef(VIRA_LATTES['Banca'])))
			g.add((banca_uri, VIRA_LATTES.ano_banca, Literal(banca_dict['ano_banca'])))
			g.add((banca_uri, VIRA_LATTES.idioma, Literal(banca_dict['idioma'], lang="pt")))
			g.add((banca_uri, VIRA_LATTES.natureza, Literal(banca_dict['natureza'], lang="pt")))
			# Relaciona a banca ao pesquisador
			g.add((pesquisador_uri, VIRA_LATTES['avalia'], banca_uri))
	else:
		g.add((pesquisador_uri, RDF.type, URIRef(VIRA_LATTES['Orientando'])))
		
	pass 

def add_publicacoes(g, publicacao_list, pesquisador_uri):
	"""
	Adiciona publicações ao grafo RDF.

	:param g: Grafo RDF onde as publicações serão adicionadas.
	:param publicacao_obj: Objeto contendo a lista de publicações.
	"""
	# Definindo o pesquisador como Orientando
	g.add((pesquisador_uri, RDF.type, URIRef(VIRA_LATTES['Orientando'])))
	
	# Iterando sobre as publicações e adicionando ao grafo
	for publicacao_dict in publicacao_list:
		publicacao_uri = URIRef(VIRA_LATTES['Publicacao'] + '/' + publicacao_dict['id'])  # URI da monografia
		g.add((publicacao_uri, RDF.type, URIRef(VIRA_LATTES['Publicacao'])))
		g.add((publicacao_uri, RDF.type, URIRef(VIRA_LATTES['Monografia'])))
		g.add((publicacao_uri, VIRA_LATTES.ano_publicacao, Literal(publicacao_dict['ano_publicacao'])))
		g.add((publicacao_uri, VIRA_LATTES.titulo_monografia, Literal(publicacao_dict['titulo'], lang="pt")))
		
		#Adicionar relação orientando - publicacao
		g.add((pesquisador_uri, VIRA_LATTES['escreve'], publicacao_uri))

		# Adicionar relação orientador - publicacao
		orientador_uri = get_or_create_orientador(g, publicacao_dict)
		
		if orientador_uri:
			g.add((orientador_uri, RDF.type, URIRef(VIRA_LATTES['Pesquisador'])))
			g.add((orientador_uri, RDF.type, URIRef(VIRA_LATTES['Orientador'])))
			g.add((orientador_uri, VIRA_LATTES['confere'], publicacao_uri))
		else:
			print(f"Orientador não encontrado para a graduação: {publicacao_dict['titulo']}")
		
		#Adiciona relcao orientador - orientando
		g.add((orientador_uri, VIRA_LATTES['orienta'], pesquisador_uri))

def get_or_create_orientador(g, publicacao_dict):
	"""
	Busca ou cria um orientador no grafo.

	:param g: Grafo RDF onde o orientador será buscado ou criado.
	:param publicacao_dict: Dicionário contendo informações da graduação.
	:return: URI do orientador encontrado ou criado.
	"""
	orientador_uri = None

	if publicacao_dict['id_orientador']:
		for s, p, o in g.triples((None, VIRA_LATTES.id_lattes, Literal(publicacao_dict['id_orientador']))):
			if s is not None:
				orientador_uri = s
				break
		if orientador_uri is None:
			orientador_uri = URIRef(VIRA_LATTES['Pesquisador'] + '/' + publicacao_dict['id_orientador'])
	else:
		orientador_nome = publicacao_dict['orientador']
		for s, p, o in g.triples((None, VIRA_LATTES.nome_pesquisador, Literal(orientador_nome, lang="pt"))):
			if s is not None:
				print(f"Orientador encontrado: {s}")
				orientador_uri = s
				break
			else:
				print(f"Orientador não encontrado: {orientador_nome}")

	return orientador_uri

if __name__ == '__main__':
	#--------------------------------------------------------------------------
	#-------------------------Manipulando o XML--------------------------------
	#--------------------------------------------------------------------------
	xml_file = 'cv/mock_lia.xml'
	# Transformando o xml em árvore 
	tree = ET.parse(xml_file)
	root = tree.getroot()
	
	# Criando um pesquisador
	pesquisador_obj = pesquisadorModule.Pesquisador()
	pesquisador_obj.get_data(root)
	
	# Criando uma banca
	banca_obj = BancaModule.Banca()
	banca_list = banca_obj.get_data(root)
	
	#Criando uma publicação
	publicacao_obj = publicacaoModule.Publicacao()
	publicacao_list = publicacao_obj.get_data(root)

	#--------------------------------------------------------------------------
	#-------------------------Manipulando o RDF--------------------------------
	#--------------------------------------------------------------------------
	
	# Abre o grafo modelado
	g = Graph()
	g.parse(location="vira-lattes-populado.ttl", format="n3")
	
	# Definindo os Namespaces
	VIRA_LATTES = Namespace("http://vira-lattes.com#")
	
	pesquisador_uri = URIRef(str(VIRA_LATTES['Pesquisador'] + "/" + pesquisador_obj.id_lattes))
	
	# Adicionando o pesquisador e suas relações ao grafo
	add_pesquisador(g, pesquisador_obj, pesquisador_uri)
	add_bancas(g, banca_list, pesquisador_uri)
	add_publicacoes(g, publicacao_list, pesquisador_uri)
	
			
	# Serializa e salva o grafo em um arquivo Turtle
	ttl = g.serialize(format="turtle")
	if isinstance(ttl, bytes):
		ttl = ttl.decode("utf-8")
	out_path = 'vira-lattes-populado.ttl'
	with open(out_path, 'w', encoding='utf-8') as saida:
		saida.write(ttl)
	print(f"Graph salvo em: {out_path}")
	