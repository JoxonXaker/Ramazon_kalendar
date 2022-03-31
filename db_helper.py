import sqlite3


class DBHelper:
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('Error: ', e)

    def get_regions(self):
        return self.cursor.execute('select id, region from regions').fetchall()

    def get_region(self, region_id):
        return self.cursor.execute('select * from regions where id=?', (region_id, )).fetchone()

    def get_calendar(self, dt):
        return self.cursor.execute('select * from ramadan_calendar where date_time = ?', (dt, )).fetchone()

    def get_full_taqvim(self):
        return self.cursor.execute('select * from ramadan_calendar').fetchall()

