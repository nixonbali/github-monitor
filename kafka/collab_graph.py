from neo4j import GraphDatabase
from dateutil.parser import parse

class CollabGraph(object):
    """Neo4j Graph Database for Collaborations"""
    def __init__(self, uri, user, password):
        """Initializes with Neo4j Bolt Address, username and password"""
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Closes connection with database"""
        self._driver.close()

    def add_action(self, event):
        """Opens Driver Session to Write to Database"""
        with self._driver.session() as session:
            return session.write_transaction(self._create_action_connection, event)

    @staticmethod
    def _create_action_connection(tx, event):
        """
        Writes Github Event to database

        Updates or Creates Repo Node
        Updates or Creates User Node
        Updates or Creates Event Connection between User and Repo
        """
        if "id" in event.value["repo"]:
            tx.run("MERGE (u:User {login: $login}) SET u.last_active = $date "
                        "MERGE (r:Repo {name:$repo_name, repo_id:$repo_id}) SET r.last_active = $date "
                        "MERGE (u)-[rel:event]->(r) "
                        "   ON CREATE SET rel.count = 1 "
                        "   ON MATCH SET rel.count = rel.count + 1 ",
                        #login=event.actor.login, date = event.created_at,
                        #repo_name = event.repo.name, repo_id=event.repo.id,
                        #event_type=event.type)
                        login=event.value["actor"]["login"],
                        date = parse(event.value["created_at"]),
                        repo_name=event.value["repo"]["name"],
                        repo_id=event.value["repo"]["id"],
                        event_type=event.value["type"])
