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
        self.comments = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def all_posts(cls):
        query = """SELECT * FROM posts LEFT JOIN users ON users.id = posts.user_id 
                LEFT JOIN comments ON comments.user_id = users.id 
                ORDER BY posts.created_at DESC;"""
        results = connectToMySQL(cls.db).query_db(query)
        # print(results)
        posts = []
        comments = []

        for row in results:
            post_data = {
                "id": row['id'],
                "content": row['content'],
                "first_name": row['first_name'],
                "user_id": row['user_id'],
                "created_at": row['created_at']
            }
            print(post_data)
            posts.append(post_data)

            if row['comments.id'] != None:
                comment_data = {
                    "id": row['comments.id'],
                    "content": row['comments.content'],
                    "first_name": row['users.first_name'],
                    "user_id": row['comments.user_id'],
                    "post_id": row['id'],
                    "created_at": row['comments.created_at']
                }
                print(comment_data)
                comments.append(comment_data)
            
        return posts, comments
    
    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        delete_data = {
            'id': data['post_id']
        }
        return connectToMySQL(cls.db).query_db(query, delete_data)
    
    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['post_content']) < 1:
            flash("Post cannot be blank")
            is_valid = False
        return is_valid