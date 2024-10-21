import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize the app
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def export_data():
    threads_ref = db.collection('threads')
    threads = threads_ref.stream()

    data = []

    for thread in threads:
        thread_id = thread.id
        messages_ref = db.collection('threads').document(thread_id).collection('messages')
        messages = messages_ref.order_by('createdAt').stream()

        message_list = []
        for message in messages:
            message_data = message.to_dict()
            message_list.append(message_data)

        data.append({
            'threadId': thread_id,
            'messages': message_list
        })

    # Save data to a JSON file
    with open('chat_data.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    export_data()
    print('Data export completed.')