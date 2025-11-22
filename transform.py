import rdflib
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, FOAF

# 1. Create a new Graph
g = Graph()

# 2. Define Namespaces (optional but good practice)
EX = Namespace("http://example.org/")
PERSON = Namespace("http://example.org/person/")
VIRA_LATTES = Namespace("http://vira_lattes.com/data/")

# Bind namespaces to the graph (for cleaner serialization)
g.bind("ex", EX)
g.bind("person", PERSON)
g.bind("foaf", FOAF)

# 3. Create URIRefs, Literals, and Blank Nodes
# Resources
john = URIRef(PERSON + "JohnDoe")
jane = URIRef(PERSON + "JaneSmith")

# Properties
name = FOAF.name
age = EX.age

# Literals
john_name = Literal("John Doe")
john_age = Literal(30)
jane_name = Literal("Jane Smith")

# 4. Add Triples to the Graph
# A triple consists of a subject, predicate, and object.
g.add((john, RDF.type, FOAF.Person))
g.add((john, name, john_name))
g.add((john, age, john_age))

g.add((jane, RDF.type, FOAF.Person))
g.add((jane, name, jane_name))
g.add((jane, FOAF.knows, john))  # Jane knows John

# 5. Serialize the Graph
# You can serialize to various formats like Turtle, RDF/XML, N-Triples, JSON-LD.
print("--- Turtle Serialization ---")
print(g.serialize(format="turtle"))

print("\n--- RDF/XML Serialization ---")
print(g.serialize(format="xml"))