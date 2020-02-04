from neomodel import StructuredNode, IntegerProperty, StringProperty, StructuredRel, RelationshipTo, RelationshipFrom
from grest import models


# class Repo()

class EventInfo(StructuredRel, models.Relation):
    """Event Information Model"""
    count = IntegerProperty()

class Repo(StructuredNode, models.Node):
    """Repo Model"""
    name = StringProperty()
    users = RelationshipFrom("User", "event")

class User(StructuredNode, models.Node):
    """User Model"""
    login = StringProperty()
    last_active = StringProperty()
    repos = RelationshipTo(Repo, "event", model=EventInfo)
