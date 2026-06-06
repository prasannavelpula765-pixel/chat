from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import threading

app = Flask(__name__)
# Enable CORS for all routes and allow all origins
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

# In-memory message storage (use database in production)
messages_store = []
users_online = {}
messages_lock = threading.Lock()

# Store active users
active_users = {
    'user1': {'id': '8106413016', 'name': 'BABU 🫠', 'avatar': '😘'},
    'user2': {'id': '8074404598', 'name': 'BEDU 🫠', 'avatar': '🥹'}
}

@app.route('/api/messages/send', methods=['POST'])
def send_message():
    """Send a message"""
    try:
        data = request.get_json()
        
        message = {
            'id': int(datetime.now().timestamp() * 1000),
            'sender': data.get('sender'),
            'text': data.get('text'),
            'msgType': data.get('msgType', 'text'),
            'mediaUrl': data.get('mediaUrl'),
            'timestamp': int(datetime.now().timestamp() * 1000),
            'sendTimestamp': int(datetime.now().timestamp() * 1000),
            'status': 'delivered',  # Message is delivered when received by server
            'deliveredTimestamp': int(datetime.now().timestamp() * 1000),
            'seenTimestamp': None,
            'seenBy': [],
            'replyToId': data.get('replyToId'),
            'hiddenForUsers': []
        }
        
        with messages_lock:
            messages_store.append(message)
        
        return jsonify({'success': True, 'message': message}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/messages/get', methods=['GET'])
def get_messages():
    """Fetch all messages"""
    try:
        user_id = request.args.get('userId')
        with messages_lock:
            # Filter out messages that are hidden for this user
            visible_messages = [
                m for m in messages_store 
                if not m.get('hiddenForUsers') or user_id not in m.get('hiddenForUsers', [])
            ]
        return jsonify({'success': True, 'messages': visible_messages}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/messages/mark-seen', methods=['POST'])
def mark_message_seen():
    """Mark message as seen"""
    try:
        data = request.get_json()
        message_id = data.get('messageId')
        user_name = data.get('userName')
        
        with messages_lock:
            for msg in messages_store:
                if msg['id'] == message_id:
                    if user_name not in msg.get('seenBy', []):
                        msg['seenBy'].append(user_name)
                        msg['status'] = 'seen'
                        msg['seenTimestamp'] = int(datetime.now().timestamp() * 1000)
                    break
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/messages/delete', methods=['POST'])
def delete_message():
    """Delete a message"""
    try:
        data = request.get_json()
        message_id = data.get('messageId')
        user_id = data.get('userId')
        delete_type = data.get('type')  # 'me' or 'everyone'
        
        with messages_lock:
            for msg in messages_store:
                if msg['id'] == message_id:
                    if delete_type == 'me':
                        if user_id not in msg['hiddenForUsers']:
                            msg['hiddenForUsers'].append(user_id)
                    elif delete_type == 'everyone':
                        if msg['sender'] == user_id:  # Only sender can delete for everyone
                            msg['text'] = '🚫 This message was deleted for everyone'
                            msg['msgType'] = 'text'
                            msg['mediaUrl'] = None
                    break
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/user/online', methods=['POST'])
def user_online():
    """Mark user as online"""
    try:
        data = request.get_json()
        user_id = data.get('userId')
        users_online[user_id] = True
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/user/offline', methods=['POST'])
def user_offline():
    """Mark user as offline"""
    try:
        data = request.get_json()
        user_id = data.get('userId')
        if user_id in users_online:
            del users_online[user_id]
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/user/status', methods=['GET'])
def user_status():
    """Check if user is online"""
    try:
        user_id = request.args.get('userId')
        is_online = users_online.get(user_id, False)
        return jsonify({'success': True, 'online': is_online}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/clear-all', methods=['POST'])
def clear_all_messages():
    """Clear all messages (for testing)"""
    try:
        with messages_lock:
            messages_store.clear()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get list of all active users"""
    try:
        users_list = []
        for user_id, user_data in active_users.items():
            users_list.append({
                'id': user_data['id'],
                'name': user_data['name'],
                'avatar': user_data['avatar'],
                'online': users_online.get(user_data['id'], False)
            })
        return jsonify({'success': True, 'users': users_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'success': True, 'status': 'Server is running'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
