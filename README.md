# GitHub Webhook Handler

A Flask application that receives GitHub webhook events and stores them in MongoDB for display.

## Features

- Receives GitHub webhook events (push, pull request, merge)
- Stores events in MongoDB with timestamps
- Web interface to view latest events
- Auto-refreshes every 15 seconds

## Prerequisites

1. **Python 3.7+**
2. **MongoDB** (running locally or accessible)
3. **GitHub repository** (to configure webhooks)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd webhook-repo
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start MongoDB:**
   - **Windows:** Start MongoDB service or run `mongod`
   - **macOS:** `brew services start mongodb-community`
   - **Linux:** `sudo systemctl start mongod`

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   - Web interface: http://localhost:5000
   - Webhook endpoint: http://localhost:5000/webhook

## GitHub Webhook Configuration

1. Go to your GitHub repository
2. Navigate to Settings → Webhooks
3. Click "Add webhook"
4. Set Payload URL to: `http://your-domain.com/webhook`
5. Select content type: `application/json`
6. Select events: `Push`, `Pull requests`
7. Click "Add webhook"

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongod --version`
- Check if MongoDB is accessible on localhost:27017
- For remote MongoDB, update the connection string in `db.py`

### Port Already in Use
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

### Webhook Not Receiving Events
- Check GitHub webhook delivery logs
- Ensure your server is publicly accessible
- Verify webhook URL is correct

## Project Structure

```
webhook-repo/
├── app.py              # Flask application
├── db.py               # MongoDB operations
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Web interface
└── README.md          # This file
```

## API Endpoints

- `GET /` - Web interface
- `GET /events` - JSON API for latest events
- `POST /webhook` - GitHub webhook endpoint

## Security Notes

- This is a basic implementation without authentication
- For production use, add webhook secret verification
- Consider rate limiting and input validation 