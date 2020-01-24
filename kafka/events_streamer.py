import faust
import json
import secrets

app = faust.App('git-app', broker=secrets.BROKER1)

events_topic = app.topic("git-events")
pr_events_topic = app.topic("pr-events")


pull_request_events = ["PullRequestEvent", "PullRequestReviewEvent", "PullRequestReviewCommentEvent"]

### Events Streamer
@app.agent(events_topic)
async def process_event(events):
    async for event in events:
        event_json = json.loads(event)
        ### Filter for PR Events and send through to PR Topic
        if (event_json['type'] in pull_request_events):
            await pr_events_topic.send(value=event_json)


### PR Events Stream Processor
#@app.agent(pr_events_topic)
#async def process_pr_events(pr_events):
#    async def for pr_event in pr_events:
#        print(pr_event)


if __name__ == "__main__":
    app.main()
