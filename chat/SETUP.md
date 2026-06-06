# Chat Application Setup Guide

## Problem Fixed
✅ **Messages now sync between different devices/mobiles** - The issue where messages weren't forwarding to the other user on a different device is now resolved!

## What Changed
The application now uses a **backend server** to sync messages between devices instead of relying on localStorage (which is device-specific).

## Installation & Running

### Step 1: Install Python Dependencies

Make sure you have Python 3.7+ installed. Then run:

```bash
pip install flask flask-cors
```

### Step 2: Start the Backend Server

Navigate to the chat directory and run:

```bash
python hm.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

**Keep this terminal open while using the chat application!**

### Step 3: Open the Chat Application

Open the frontend in your browser:

**Option A: From File System**
- Open `frontend/index.html` directly in your browser

**Option B: Using a Local Server (Recommended)**
```bash
# In another terminal, run a simple Python HTTP server
python -m http.server 8000
# Then open http://localhost:8000/frontend/
```

### Step 4: Test with Two Users

To test messaging between two users on different devices:

1. **Device/Browser 1**: Open the chat and login as:
   - User ID: `8106413016`
   - Password: `surya`

2. **Device/Browser 2**: Open the chat and login as:
   - User ID: `8074404598`
   - Password: `arun`

3. **Send messages** from one device - they will now appear on the other device in real-time!

## How It Works

### Backend API Endpoints

- `POST /api/messages/send` - Send a new message
- `GET /api/messages/get?userId=XXX` - Fetch all messages
- `POST /api/messages/mark-seen` - Mark message as seen
- `POST /api/messages/delete` - Delete a message
- `POST /api/user/online` - Mark user as online
- `POST /api/user/offline` - Mark user as offline
- `GET /api/user/status?userId=XXX` - Check if user is online

### Message Flow

1. User 1 types a message and clicks Send
2. Frontend sends the message to the backend API
3. Backend stores the message in memory
4. User 2's frontend polls the backend every 1 second
5. New messages are fetched and displayed in real-time

## Troubleshooting

### "Failed to send message. Make sure backend server is running..."
- Make sure the Flask backend is running on http://localhost:5000
- Run `python hm.py` in the chat directory

### Messages not appearing on other device
- Check that both devices are accessing the same backend (http://localhost:5000)
- If on different WiFi networks, update `API_BASE_URL` in `frontend/index.html` to use your machine's IP address instead of localhost
- Ensure the backend server is running

### Port 5000 already in use
Run Flask on a different port:
```bash
# In hm.py, change the last line to:
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Changed from 5000 to 5001

# Then update API_BASE_URL in frontend/index.html:
const API_BASE_URL = 'http://localhost:5001/api';
```

## For Production Deployment

For real-world use, replace the in-memory storage with a proper database:

```python
# Instead of:
messages_store = []

# Use a database like SQLite, PostgreSQL, or MongoDB
```

Also consider:
- Using WebSockets for real-time updates instead of polling
- Adding authentication/JWT tokens
- Encrypting messages
- Deploying to a cloud server (Heroku, AWS, DigitalOcean, etc.)
