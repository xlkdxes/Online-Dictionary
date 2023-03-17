import pymysql


class DictDB:
    def __init__(self):
        self.kwargs = {
            'user': 'root',
            'password': '123456',
            'database': 'dictproject',
            'charset': 'utf8'
        }
        self.db = pymysql.connect(**self.kwargs)
        self.cur = self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    def register(self, username, password):
        sql = 'INSERT INTO users (username, password) VALUES(%s, %s);'
        try:
            self.cur.execute(sql, [username, password])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def login(self, username, password):
        sql = 'SELECT * FROM users WHERE BINARY username = %s AND password = %s'
        self.cur.execute(sql, (username, password))
        if self.cur.fetchone():
            return True
        else:
            return False

    def insert_words(self):
        with open('dict.txt', 'r') as fr:
            for line in fr:
                word, exp = line.split(' ', 1)
                exp = exp.strip()
                sql = 'INSERT INTO words (word, explaination) VALUES (%s, %s)'
                try:
                    self.cur.execute(sql, [word, exp])
                    self.db.commit()
                except:
                    pass

    def query(self, word, name):
        sql = 'SELECT word_id, explaination FROM words WHERE word = %s'
        self.cur.execute(sql, [word])
        result = self.cur.fetchone()
        word_id = result[0]
        self.insert_history(word_id, name)
        if result:
            return result[1]

    def insert_history(self, word_id, name):
        sql = 'SELECT user_id FROM users WHERE username = %s'
        self.cur.execute(sql, [name])
        user_id = self.cur.fetchone()[0]
        sql2 = 'INSERT INTO queryhistory(user_id, word_id) VALUES(%s, %s)'
        self.cur.execute(sql2, [user_id, word_id])
        self.db.commit()

    def history(self, name):
        sql = 'SELECT username, word, query_time FROM queryhistory q ' \
              'JOIN users u USING (user_id) JOIN words w USING (word_id) ' \
              'WHERE u.username = %s ORDER BY q.query_time DESC LIMIT 10'
        self.cur.execute(sql, [name])
        data = self.cur.fetchall()
        return data
