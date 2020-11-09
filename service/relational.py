
diagram = {
  "email": "omar@email.tv",
  "diagram": {
    "class": "GraphLinksModel",
    "modelData": {
      "position": "-659.5028514418491 -993.572273697964"
    },
    "nodeDataArray": [
      {
        "type": "entity",
        "text": "Student",
        "figure": "Rectangle",
        "fill": "white",
        "key": -1,
        "loc": "-460 -760"
      },
      {
        "type": "atribute",
        "text": "id",
        "figure": "Ellipse",
        "fill": "white",
        "key": -3,
        "loc": "-610 -780"
      },
      {
        "type": "entity",
        "text": "Subject",
        "figure": "Rectangle",
        "fill": "white",
        "key": -4,
        "loc": "0 -760"
      },
      {
        "type": "atribute",
        "text": "Full_name",
        "figure": "Ellipse",
        "fill": "white",
        "key": -5,
        "loc": "-480 -590"
      },
      {
        "type": "relation",
        "text": "Have",
        "figure": "Diamond",
        "fill": "white",
        "key": -8,
        "loc": "-220 -760"
      },
      {
        "type": "atribute",
        "text": "id",
        "figure": "Ellipse",
        "fill": "white",
        "key": -6,
        "loc": "150 -800"
      },
      {
        "type": "atribute",
        "text": "Name_class",
        "figure": "Ellipse",
        "fill": "white",
        "key": -7,
        "loc": "100 -650"
      }
    ],
    "linkDataArray": [
      {
        "from": -1,
        "to": -3
      },
      {
        "from": -1,
        "to": -5
      },
      {
        "from": -6,
        "to": -4
      },
      {
        "from": -4,
        "to": -7
      },
      {
        "from": -1,
        "to": -8
      },
      {
        "from": -8,
        "to": -4
      }
    ]
  }
}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getSentencesSQL(project_name, entitiesWithAttrs):
  database_template = """
  CREATE DATABASE {db_name};
  USE {db_name};
  """

  script_sentences = database_template.format(db_name=project_name)

  for table in entitiesWithAttrs:
    print(table)
    # get name table in dict with next(iter(table))
    # table_script = table_template.format(next(iter(table)), getColumns(list(table.values())) )
    script_sentences += build_table_sentence(table)

  return script_sentences

def build_table_sentence(table_dict):

  table_template = """
  -- step 1. drop table if exists
  DROP TABLE IF EXISTS {table_name} CASCADE;
  --step 2. create table 
  CREATE TABLE [IF NOT EXISTS] {table_name} (
  --step 3. create columns dinamically with next nomenclature
  -- column_name data_type(length) [NOT NULL] [DEFAULT value] [AUTO_INCREMENT] column_constraint;
  {attrs_sentences}
  ) ENGINE=InnoDB;
  """
  attr_by_table = ""
  # for table in table_dict:
  #   attr_by_table = getColumns()

  return table_template.format(table_name=next(iter(table_dict)), attrs_sentences='')
def getEntities(diagram):
  entities = []
  for node in diagram['diagram']['nodeDataArray']:
    if node['type'] == 'entity':
      entities.append(
        (node['text'], node['key'])
        )
  return entities

def getAttrs(diagram):
  attrs = []
  for node in diagram['diagram']['nodeDataArray']:
    if node['type'] in ['atribute', 'atributeDerived', 'keyAttribute', 'atributeComposite']:
      attrs.append(
        (node['text'], node['key'])
        )
  return attrs

def getRelationships(diagram):
  relationships = []
  for node in diagram['diagram']['nodeDataArray']:
    if node['type'] in ['relation']:
      print(bcolors.OKGREEN + 'relationship correct' + bcolors.ENDC) if validateOnlyBinarieRelationship(node['key'], diagram) else print(bcolors.FAIL + 'relationship error' + bcolors.ENDC)
      relationships.append(
        (node['text'], node['key'])
        )
  return relationships

def validateOnlyBinarieRelationship(relationKey, diagram):
  count = 0
  for node in diagram['diagram']['linkDataArray']:
    if node['from'] == relationKey or node['to'] == relationKey:
      count += 1
  return True if count == 2 else False


def getEntityWithAtributes(diagram, entity, attrs):
  print(f"{bcolors.OKCYAN} {entity} {bcolors.ENDC}")
  diagramDict = diagram['diagram']
  entityWithAttr = []
  for node in diagramDict['linkDataArray']:  #pattern matching from & to 
    origin, destiny = node.items()
    if origin[1] == entity[1]:
      print("match %s entity with attr %s - %s"% (entity[0], origin[1], destiny[1]) )
      for attr in attrs:
        if attr[1] == destiny[1]:
          entityWithAttr.append(attr)
    if destiny[1] == entity[1]:
      print("match %s entity with attr %s - %s"% (entity[0], destiny[1], origin[1]) )
      for attr in attrs:
        if attr[1] == origin[1]:
          entityWithAttr.append(attr)

projectName = "test_sql"

entities = getEntities(diagram)
attrs = getAttrs(diagram)
relations = getRelationships(diagram)
entitiesWithAttrs = [getEntityWithAtributes(diagram, entity, attrs) for entity in entities]

script_sql_sentences = getSentencesSQL(projectName, entitiesWithAttrs)

print("*"*20)
print(entitiesWithAttrs)
print(script_sql_sentences)