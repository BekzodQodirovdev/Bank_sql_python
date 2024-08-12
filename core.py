import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self) -> None:
        self.connect()

    def connect(self):
        self.connetion = mysql.connector.connect(
            host = "localhost",
            user = 'root',
            password = "root",
            database = 'payme'
        )

    def insert_user(self, user: dict):
        self.connect()
        try:
            with self.connetion.cursor() as cursor:
                query = '''
                    INSERT INTO users (username, email, password, card_num, card_pwd) VALUES 
                    (%s, %s, %s, %s, %s)
                '''
                cursor.execute(query, (user['username'], user['email'], user['password'],user['card_num'],user['card_pwd']))
                self.connetion.commit()
                self.connetion.close()
                return False
        except Error as err:
            self.connetion.close()
            return True
        
    def is_user(self,user: dict) -> int:
        self.connect()
        try:
            with self.connetion.cursor() as cursor:
                query = '''
                    SELECT id FROM users WHERE email = %s AND password = %s;
                '''
                cursor.execute(query,(user['email'],user['password']))
                _id = cursor.fetchone()
            self.connetion.close()
            if not _id:
                return False
            return _id[0]
        except Error as err:
            self.connetion.close()
            return False
        
    def is_admin(self, _id):
        self.connect()
        try:
            with self.connetion.cursor() as cursor: 
                query = '''
                    SELECT a.id
                    FROM admin as a
                    JOIN users as u
                    ON a.id = u.id
                    WHERE a.id = %s
                '''
                cursor.execute(query, (_id,)) 
                id = cursor.fetchone()
            self.connetion.close() 
            if id:
                return True
            else:
                return False 
            # return id  
                
        except Error as err:
            self.connetion.close()
            return False

    def get_users(self):
        self.connect()
        try:
            with self.connetion.cursor() as cursor:
                query = '''SELECT id, name, username FROM users'''
                cursor.execute(query)
                users = cursor.fetchall()
            self.connetion.close()
            return users
        except Error as err:
            return []
        
    def update_user(self, user: dict):
        self.connect()
        try:
            with self.connetion.cursor() as cursor:
                query = '''
                    UPDATE users
                    SET name = %s, username = %s, password = %s
                    WHERE id = %s
                '''
                cursor.execute(query, (user['name'], user['login'], user['pwd'], user['id']))
                self.connetion.commit()
                self.connetion.close()
                return False
        except Error as err:
            return True
        
    def del_user(self,id):
        self.connect()
        try:
            with self.connetion.cursor() as cursor:
                query = '''DELETE FROM users WHERE id = %s'''
                cursor.execute(query,(id,))
                self.connetion.commit()
            self.connetion.close()
                # return 0
        except Error as err:
            return -1

    def search_data(self,query_data):
        self.connect()
        try:
            with self.connetion.cursor() as cursor:
                query = '''SELECT * FROM users WHERE username LIKE '%{%s}%' OR email LIKE '%{%s}%'''
                cursor.execute(query,(query_data['query']))
                users = cursor.fetchone()
            self.connetion.close()
            return users
        except Error as err:
            return -1  
        
    # import mysql.connector

class DATA:
    def __init__(self):
        self.conc()
    
    def conc(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='payme'
        )
        self.cursor = self.conn.cursor()


    # def search_data(self,query_data):
    #     self.conc()
    #     try:
    #         with self.conn.cursor() as cursor:
    #             query = f'''SELECT * FROM users WHERE username LIKE '%{query_data['query']}%' OR email LIKE '%{query_data['query']}%'''
    #             cursor.execute(query)
    #         users = cursor.fetchall()
    #         self.conn.close()
    #         print(users)
    #         return users
    #     except Error as err:
    #         return str(err)

    def search_data(self, data):
        query = f"SELECT * FROM users WHERE username LIKE '%{data['query']}%' OR email LIKE '%{data['query']}%'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_data(self, id_, new_values):
        query = """
        UPDATE users 
        SET username = %s, email = %s, password = %s, card_num = %s, card_pwd = %s, amount = %s 
        WHERE id = %s
        """
        self.cursor.execute(query, (*new_values, id_))
        self.conn.commit()

    def delete_data(self, id_):
        query = "DELETE FROM users WHERE id = %s"
        self.cursor.execute(query, (id_,))
        self.conn.commit()

    

# CREATE TABLE users (
#     id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
#     username VARCHAR(64) UNIQUE,
#     email VARCHAR(64),
#     password VARCHAR(64),
#     card_num VARCHAR(64),
#     card_pwd VARCHAR(64)
# )