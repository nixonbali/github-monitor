from neomodel import ZeroOrMore, StructuredNode, IntegerProperty, StringProperty, StructuredRel, RelationshipTo, RelationshipFrom
from grest import models
from webargs import fields


# class Repo()

class EventInfo(StructuredRel, models.Relation):
    """Event Information Model"""
    count = IntegerProperty()

class Repo(StructuredNode, models.Node):
    """Repo Model"""
    id = IntegerProperty()
    name = StringProperty()
    #users = RelationshipFrom("User", "event", cardinality=ZeroOrMore)

class User(StructuredNode, models.Node):
    """User Model"""
    login = StringProperty()
    last_active = StringProperty()
    repos = RelationshipTo(Repo, "event", model=EventInfo, cardinality=ZeroOrMore)


    # def repos(self):
    #     results, columns = self.cypher("MATCH p=(n:User)-->() where id(n) = {self} RETURN p")
    #     return [self.inflate(row[0]) for row in results]
