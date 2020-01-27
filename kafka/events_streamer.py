import faust
import json
import secrets
from event_types import *

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
@app.agent(collab_topic)
async def process_collab(collabs):
    async for collab in collabs:
        print(collab.actor.login)
        # client = aredis.StrictRedis(host="localhost", port=6379)
        # await client.zadd(activity.user, activity.timestamp, activity.message)




### PR Events Stream Processor
#@app.agent(pr_events_topic)
#async def process_pr_events(pr_events):
#    async def for pr_event in pr_events:
#        print(pr_event)


if __name__ == "__main__":
    app.main()
