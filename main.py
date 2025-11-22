#Importando outras classes
import src.publication as publication
import src.curriculum as curriculum
import src.pesquisador as pesquisadorModule
import src.banca as BancaModule
# #Importando libs
import xml.etree.ElementTree as ET
import rdflib
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, OWL

if __name__ == '__main__':
	#--------------------------------------------------------------------------
	#-------------------------Manipulando o XML--------------------------------
	#--------------------------------------------------------------------------
	xml_file = 'cv/gabriela.xml'
	# Transformando o xml em árvore 
	tree = ET.parse(xml_file)
	root = tree.getroot()
	
	# Criando um pesquisador
	pesquisador_obj = pesquisadorModule.Pesquisador()
	pesquisador_obj.get_data(root)
	
	# Criando uma banca
	banca_obj = BancaModule.Banca()
	banca_list = banca_obj.get_data(root)

	#--------------------------------------------------------------------------
	#-------------------------Manipulando o RDF--------------------------------
	#--------------------------------------------------------------------------
	# Abre o grafo modelado
	g = Graph()
	g.parse(location="vira-lattes2.ttl", format="n3")
	
	# Definindo os Namespaces
	VIRA_LATTES = Namespace("http://vira-lattes.com#")
	
	pesquisador_uri = URIRef(str(VIRA_LATTES['Pesquisador'] + "/" + pesquisador_obj.id_lattes))
	
	# Adicionando o pesquisador ao grafo
	if pesquisador_obj.role == 'Avaliador':
		g.add((pesquisador_uri, RDF.type, URIRef(VIRA_LATTES['Avaliador'])))
		
		# Iterando sobre as bancas e adicionando ao grafo
		for banca_dict in banca_list:
			banca_uri = URIRef(VIRA_LATTES['Banca'] + '/' +banca_dict['id_banca'])  # URI da banca
			g.add((banca_uri, RDF.type, URIRef(VIRA_LATTES['Banca'])))
			g.add((banca_uri, VIRA_LATTES.ano, Literal(banca_dict['ano_banca'])))
			g.add((banca_uri, VIRA_LATTES.idioma, Literal(banca_dict['idioma'], lang="pt")))
			g.add((banca_uri, VIRA_LATTES.natureza, Literal(banca_dict['natureza'], lang="pt")))
			
			# Relaciona a banca ao pesquisador
			g.add((pesquisador_uri, VIRA_LATTES['avalia'], banca_uri))
			
	else:
		g.add((pesquisador_uri, RDF.type, URIRef(VIRA_LATTES['Orientando'])))
	# g.add((pesquisador_uri, RDF.type, URIRef(VIRA_LATTES['Pesquisador'])))
	g.add((pesquisador_uri, VIRA_LATTES.nome_pesquisador, Literal(pesquisador_obj.nome, lang="pt")))
	g.add((pesquisador_uri, VIRA_LATTES.id_lattes, Literal(pesquisador_obj.id_lattes)))
	g.add((pesquisador_uri, VIRA_LATTES.nacionalidade, Literal(pesquisador_obj.nacionalidade, lang="pt")))
	g.add((pesquisador_uri, VIRA_LATTES.atualizacao, Literal(pesquisador_obj.data_atualizacao)))
	
			
	# Serializa e salva o grafo em um arquivo Turtle
	ttl = g.serialize(format="turtle")
	if isinstance(ttl, bytes):
		ttl = ttl.decode("utf-8")
	out_path = 'output/gabi.ttl'
	with open(out_path, 'w', encoding='utf-8') as saida:
		saida.write(ttl)
	print(f"Graph salvo em: {out_path}")

	# #navegando pelas triplas
	# for s, p, o in g:
	# 	print(s, p, o)
	# 	break
	
	# if (URIRef('http://vira-lattes.com/pesquisador/2469487264010076'), None, None) in g:
	# 	print('Encontrado pesquisador')
	# else:
	# 	print('Pesquisador não encontrado')	
		
		
	# print(len(g))
	# propertys = set()
	# for s, p, o in g:
	# 	propertys.add(p)
	# # pprint(propertys)
	# # print(len(propertys))