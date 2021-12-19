from py2neo import Graph, Node, Relationship, Subgraph


def __neo4j():
    url = "bolt://3.239.77.82:7687"
    pwd = "hardness-changes-management"
    graph = Graph(url, auth=('neo4j', pwd))

    return graph


def neo4j_add_node(type: str, name: str):
    graph = __neo4j()
    a = Node(f"{type}", name=name)

    return graph.create(a)


def neo4j_delete_node(type: str, name: str):
    graph = __neo4j()
    node = graph.evaluate("Match (n: " + f"{type}" + "{name: " + f"'{name}'" + "}) Return n")

    return graph.delete(node)


def neo4j_create_relationship(name_1: str, name_2: str, relation: str):
    graph = __neo4j()

    return graph.run("Match (p: Person),(m: Map) Where p.name = " + f'"{name_1}"' + " and m.name = " + f'"{name_2}"'
                     + " Create (p)-[r:" + f"{relation}" + "]->(m) Return type(r)")


def neo4j_delete_relationship(name: str, relation: str):
    graph = __neo4j()

    return graph.run("Match (p: Person {name: " + f"'{name}'" + "})-[r:" + f"{relation}" + "]->() Delete r")


def neo4j_get_all_childs(name: str, relation: str):
    graph = __neo4j()

    return graph.run("Match c=()-[r: " + f"{relation}" + "]->(m: Map {name: " + f"'{name}'" + "}) Return c")

# neo4j_add_node("Person", "Dima")
# neo4j_add_node("Map", "Dust2x2")
# print(neo4j_create_relationship("Dima", "Dust2x2", "December_21"))
# neo4j_delete_node("Person", "Denis")
# neo4j_delete_relationship("Denis", "Play")
# print(neo4j_get_all_childs("Dust2x2", "December_21"))
