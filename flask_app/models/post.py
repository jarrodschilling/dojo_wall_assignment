from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, comment

class Post:
    db = 'dojo_wall_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.comment = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def all_posts(cls):
        query = "SELECT * FROM posts LEFT JOIN users ON users.id = posts.user_id;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        posts = []

        for row in results:
            post_data = {
                "content": row['content'],
                "first_name": row['first_name'],
                "created_at": row['created_at']
            }
            print(post_data)
            posts.append(post_data)
        
        return posts