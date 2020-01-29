import faust
import json
import secrets
from event_types import *
from collab_graph import CollabGraph

app = faust.App('git-app', broker=secrets.BROKER1)

events_topic = app.topic("git-events")
pr_events_topic = app.topic("pr-events", value_type=PREvent)
collab_topic = app.topic("collab", value_type=GeneralEvent)

pull_request_events = ["PullRequestEvent", "PullRequestReviewEvent", "PullRequestReviewCommentEvent"]

### Events Streamer
@app.agent(events_topic)
async def process_event(events):
    async for event in events:
        event_json = json.loads(event)
        ### Filter for PR Events and send through to PR Topic
        if (event_json['type'] in pull_request_events):
            await pr_events_topic.send(value=event_json)
        # write all events user + repo to new topic to gather user / repo info to build graph
        # read in event_json as new type
        await collab_topic.send(value=event_json)


### Graph writer
# @app.agent(collab_topic)
# async def process_collab(events):
#     async for event in events:
#         #print(collab.actor.login)
#         Graph = CollabGraph(secrets.NEO4J_BROKER, secrets.NEO4J_USER, secrets.NEO4J_PASSWORD)
#         Graph.add_action(event)
        # client = aredis.StrictRedis(host="localhost", port=6379)
        # await client.zadd(activity.user, activity.timestamp, activity.message)




### PR Events Stream Processor
#@app.agent(pr_events_topic)
#async def process_pr_events(pr_events):
#    async def for pr_event in pr_events:
#        print(pr_event)


if __name__ == "__main__":
    app.main()
