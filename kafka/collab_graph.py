from neo4j import GraphDatabase

class CollabGraph(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def add_action(self, event):
        with self._driver.session() as session:
            return session.write_transaction(self._create_action_connection, event)

    @staticmethod
    def _create_action_connection(tx, event):
        return tx.run("MERGE (u:User {login: $login}) SET u.last_active = $date "
                        "MERGE (r:Repo {name:$repo_name, id:$repo_id}) SET u.last_active = $date "
                        "MERGE (u)-[rel:event]->(r) "
                        "   ON CREATE SET rel.count = 1 "
                        "   ON MATCH SET rel.count = rel.count + 1 ",
                        #login=event.actor.login, date = event.created_at,
                        #repo_name = event.repo.name, repo_id=event.repo.id,
                        #event_type=event.type)
                        login=event.value["actor"]["login"],
                        date = event.value["created_at"],
                        repo_name=event.value["repo"]["name"],
                        repo_id=event.value["repo"]["id"],
                        event_type=event.value["type"])
