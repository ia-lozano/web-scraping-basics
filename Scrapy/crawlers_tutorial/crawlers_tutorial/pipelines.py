# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import sqlite3

# Remember to install pydns and pymongo

class MongodbPipeLine:
    collection_name = 'transcripts'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://user:user@cluster0.ah9wd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        self.db = self.client['MyMongoDB']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item

# To save data in SQLite
class SQLitePipeLine:

    def open_spider(self, spider):
        self.connection = sqlite3.connect('transcripts.db')
        self.c = self.connection.cursor()
        # query
        try:
            self.c.execute('''
                CREATE TABLE transcripts(
                title TEXT,
                plot TEXT,
                script TEXT,
                url TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO transcripts (title, plot, script, url) VALUES(?,?,?,?)
        ''', (
            item.get('title'),
            item.get('plot'),
            item.get('script'),
            item.get('url')
        ))
        self.connection.commit()
        return item

