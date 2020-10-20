#!/usr/bin python3
# -*- coding: utf-8 -*-

'''

Файл для функций базы данных
[id, item_name, ozon_token, min_price, 
ozon_link, citilink_link, beru_link, dns_link, 
ozon_price_start, citilink_price_start, beru_price_start, dns_price_start, 
ozon_price_now, citilink_price_now, beru_price_now, dns_price_now, 
create_at, update_at]
'''

import sqlite3 as sl
import configparser

class SQLer:

    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.conn = sl.connect(self.config['DATABASE']['DBNAME'])
        self.table_name = self.config['DATABASE']['DBTABLE']

    
    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sl.connect(db_file)
        except sl.Error as e:
            print(e)

        return conn


    def _create_table(self, conn):
        # conn = self.conn
        with conn:
            conn.execute("""
                
                CREATE TABLE SHOPO (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT,
                    ozon_token TEXT,
                    min_price INTEGER,

                    ozon_link TEXT,
                    citilink_link TEXT,
                    beru_link TEXT,
                    dns_link TEXT,

                    ozon_price_start TEXT,
                    citilink_price_start TEXT,
                    beru_price_start TEXT,
                    dns_price_start TEXT,

                    ozon_price_now TEXT,
                    citilink_price_now TEXT,
                    beru_price_now TEXT,
                    dns_price_now TEXT,

                    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                );

            """)

            conn.execute("""
                CREATE TRIGGER [UpdateLastTime]  
                    AFTER   
                    UPDATE  
                    ON SHOPO
                    FOR EACH ROW   
                    WHEN NEW.update_at <= OLD.update_at  
                BEGIN  
                    update SHOPO set update_at=CURRENT_TIMESTAMP where id=OLD.id;  
                END
            """)


    def _insert_test_data(self, conn):
        
        DNS_URL = "https://technopoint.ru/product/900e8d77d4411b80/102-planset-apple-ipad-2019-32-gb--zolotistyj-sale/"
        OZON_URL = "https://www.ozon.ru/context/detail/id/160020615/"
        BERU_URL = "https://beru.ru/product/planshet-apple-ipad-2019-32gb-wi-fi-silver/100774721748"
        CITILINK_URL = "https://www.citilink.ru/catalog/mobile/tablet_pc/1179782/"     

        sql = 'INSERT INTO {} ( \
            item_name, min_price, \
            ozon_link, citilink_link, beru_link, dns_link) \
            values (?, ?, ?, ?, ?, ?)'.format(self.table_name)

        data = ("Планшет Apple iPad 2019",
                27990, 
                OZON_URL, CITILINK_URL, BERU_URL, DNS_URL)
        

        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()

        return cur.lastrowid


    def create_item(self, conn, item):
        """
        Create a new task
        :param conn:
        :param item: 
        :values item_name, ozon_token, min_price, ozon_link, citilink_link, beru_link, dns_link:
        :return:
        """

        sql = '''
        INSERT INTO {} (item_name, min_price, \
            ozon_link, citilink_link, beru_link, dns_link)
                VALUES(?,?,?,?,?,?)
            '''.format(self.table_name)

        cur = conn.cursor()
        cur.execute(sql, item)
        conn.commit()

        return cur.lastrowid


    


    
    def select_all_items(self, conn):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM SHOPO")

        rows = cur.fetchall()

        for row in rows:
            print(row)


    def select_data_by_id(self, conn, id):
        id = str(id)
        cur = conn.cursor()
        cur.execute("SELECT * FROM {} WHERE id = ?".format(self.table_name), (id))
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return row


    def select_data_by_ozon_link(self, conn, ozon_link):
        cur = conn.cursor()
        cur.execute("SELECT * FROM {} WHERE ozon_link = ?".format(self.table_name), [ozon_link])
        rows = cur.fetchall()
        if len(rows) == 1:
            return rows[0]
        else:
            return 0
    

    def update_data(self, conn, item):
        # conn = self.conn

        sql = '''
        UPDATE {} SET 
            min_price = ?,
            
            ozon_link = ?,
            citilink_link = ?,
            beru_link = ?,
            dns_link = ?,

            ozon_price_start = ?,
            citilink_price_start = ?,
            beru_price_start = ?,
            dns_price_start = ?,

            ozon_price_now = ?,
            citilink_price_now = ?,
            beru_price_now = ?,
            dns_price_now = ?

        WHERE id = ?
        '''.format(self.table_name)
    
        cur = conn.cursor()
        cur.execute(sql, item)
        conn.commit()
        
    
    def delete_data(self, conn, id):
        """
        Delete a task by task id
        :param conn:  Connection to the SQLite database
        :param id: id of the task
        :return:
        """
        id = str(id)
        sql = 'DELETE FROM {} WHERE id=?'.format(self.table_name)
        cur = conn.cursor()
        cur.execute(sql, (id))
        conn.commit()


##################################
def test_insert(config, conn, sql):
    DNS_URL = "https://technopoint.ru/product/8954c13119623332/paroocistitel-karcher-sc-2-de-luxe-zeltyj-sale/"
    OZON_URL = "https://www.ozon.ru/context/detail/id/150288308/"
    BERU_URL = "https://beru.ru/product/paroochistitel-karcher-sc-2-deluxe-easyfix/100565630777"
    CITILINK_URL = "https://www.citilink.ru/catalog/large_and_small_appliances/home_appliances/steam_cleaners/1182456/"

    data = ("Пароочиститель KARCHER SC 2", 
                8970, 
                OZON_URL, CITILINK_URL, BERU_URL, DNS_URL)

    sql.create_item(conn, data)


def test_update(config, conn, sql, id):
    item = sql.select_data_by_id(conn, id)

    data = (
        item[3],
        item[4],
        item[5],
        item[6],
        item[7],

        8970,
        10250, 
        11490, 
        11499, 

        8971,
        10240,
        11490,
        11499,

        id
    )

    sql.update_data(conn, data)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    sql = SQLer()
    conn = sql.create_connection(config['DATABASE']['DBNAME'])
    
    # sql.create_table()
    # sql._insert_test_data(conn)
    

    # test_insert(config, conn, sql)
    # sql.delete_data(conn, 6)

    # sql.select_all_items(conn)
    # om = sql.select_data_by_id(conn, 1)
    # sql.select_data_by_id(conn, 2)

    # test_update(config, conn, sql, 7)

if __name__ == '__main__':
    main()


