from flask import Flask, request, jsonify, render_template
from db import insert_event, get_latest_events
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/events", methods=["GET"])
def fetch_events():
    events = get_latest_events()
    for event in events:
        event["_id"] = str(event["_id"])  
        event["timestamp"] = event["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")
    return jsonify(events)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Verify content type
    if not request.is_json:
        return "Content-Type must be application/json", 400
    
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.get_json()

    if not payload:
        return "Invalid payload", 400

    # Log incoming webhook for debugging
    print(f"Received {event_type} event from GitHub")

    try:
        event_data = None
        
        if event_type == "push":
            # Handle push events
            if "pusher" not in payload or "ref" not in payload:
                return "Invalid push payload", 400
                
            event_data = {
                "type": "push",
                "author": payload["pusher"]["name"],
                "to_branch": payload["ref"].split("/")[-1],
                "repository": payload.get("repository", {}).get("name", "unknown")
            }

        elif event_type == "pull_request":
            # Handle pull request events
            if "pull_request" not in payload or "action" not in payload:
                return "Invalid pull request payload", 400
                
            pr = payload["pull_request"]
            action = payload["action"]

            if action == "opened":
                event_data = {
                    "type": "pull_request",
                    "author": pr["user"]["login"],
                    "from_branch": pr["head"]["ref"],
                    "to_branch": pr["base"]["ref"],
                    "repository": payload.get("repository", {}).get("name", "unknown")
                }

            elif action == "closed" and pr.get("merged"):
                event_data = {
                    "type": "merge",
                    "author": pr["user"]["login"],
                    "from_branch": pr["head"]["ref"],
                    "to_branch": pr["base"]["ref"],
                    "repository": payload.get("repository", {}).get("name", "unknown")
                }
            else:
                print(f"Ignoring pull request action: {action}")
                return "Ignored action", 204

        else:
            print(f"Unhandled event type: {event_type}")
            return "Event not handled", 204

        if event_data:
            insert_event(event_data)
            print(f"Successfully recorded {event_type} event")
            return "Event recorded", 200

    except KeyError as e:
        print(f"Missing required field in payload: {e}")
        return f"Missing required field: {str(e)}", 400
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
