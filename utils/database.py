from pymongo import MongoClient
import logging

class DBHelper:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client['telegram_bot']
        self.users = self.db['users']
        self.blocked_users = self.db['blocked_users']
        self.button4_content = self.db['button4_content'] 
        self.button3_content = self.db['button3_content']
        self.button2_content = self.db['button2_content']
        self.button1_content = self.db['button1_content']
        self.welcome_content = self.db['welcome_content']

    def user_exists(self, user_id):
        return self.users.find_one({"user_id": user_id}) is not None

    def add_user(self, user_id, username, first_name):
        if not self.user_exists(user_id):
            self.users.insert_one({"user_id": user_id, "username": username, "first_name": first_name})

    def get_all_subscribers(self):
        return [user['user_id'] for user in self.users.find()]

    def move_user_to_blocked_table(self, user_id):
        try:
            user = self.users.find_one({"user_id": user_id})
            if user:
                self.users.delete_one({"user_id": user_id})
                self.blocked_users.insert_one(user)
        except Exception as e:
            logging.error(f"Error occurred while moving user: {e}")

    def add_button4_content(self, user_id, content_type, caption, photo, video):
        self.button4_content.insert_one({"user_id": user_id, "content_type": content_type, "caption": caption, "photo":photo, "video":video})
    
    def add_button3_content(self, user_id, content_type, caption, photo, video):
        self.button3_content.insert_one({"user_id": user_id, "content_type": content_type, "caption": caption, "photo":photo, "video":video})
    
    def add_button2_content(self, user_id, content_type, caption, photo, video):
        self.button2_content.insert_one({"user_id": user_id, "content_type": content_type, "caption": caption, "photo":photo, "video":video})
    
    def add_button1_content(self, user_id, content_type, caption, photo, video):
        self.button1_content.insert_one({"user_id": user_id, "content_type": content_type, "caption": caption, "photo":photo, "video":video})
    
    def add_welcome_content(self, user_id, content_type, caption, photo, video):
        self.welcome_content.insert_one({"user_id": user_id, "content_type": content_type, "caption": caption, "photo":photo, "video":video})
    
    def get_button1_content(self):
        return self.button1_content.find()
    
    def get_button2_content(self):
        return self.button2_content.find()

    def get_button3_content(self):
        return self.button3_content.find()
    
    def get_button4_content(self):
        return self.button4_content.find()
    
    def get_welcome_content(self):
        return self.welcome_content.find()
