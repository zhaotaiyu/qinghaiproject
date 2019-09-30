# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json
import pymongo
import psycopg2
from pykafka import KafkaClient
from .settings import *
from qinghaiproject.items import *
from pykafka.exceptions import SocketDisconnectedError, LeaderNotAvailable

class QinghaiprojectPipeline(object):
    def process_item(self, item, spider):
        item["create_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["modification_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["is_delete"] = 0
        item["status"] = 1
        if not isinstance(item,BeianItem):
            item["source"] = "青海"
        for key,value in item.items():
            if value in [None,""]:
                item[key] = "None"
        return item
class PgsqlPipeline(object):
    def __init__(self, pgsql_uri, pgsql_db,pgsql_user,pgsql_pass,pgsql_port):
        self.pgsql_uri = pgsql_uri
        self.pgsql_db = pgsql_db
        self.pgsql_user = pgsql_user
        self.pgsql_pass = pgsql_pass
        self.pgsql_port=pgsql_port
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            pgsql_uri=crawler.settings.get('PGSQL_URI'),
            pgsql_db=crawler.settings.get('PGSQL_DATABASE'),
            pgsql_user =crawler.settings.get('PGSQL_USER'),
            pgsql_pass=crawler.settings.get('PGSQL_PASS'),
            pgsql_port=crawler.settings.get('PGSQL_PORT')
        )
    def open_spider(self, spider):
        # 创建连接对象
        self.db = psycopg2.connect(database=self.pgsql_db, user=self.pgsql_user, password=self.pgsql_pass, host=self.pgsql_uri, port=self.pgsql_port)
        self.cursor = self.db.cursor()
        print("已连接数据库")
    def close_spider(self, spider):
        print("已关闭数据库")
        self.cursor.close()
        self.db.close()
    def process_item(self,item,spider):
        ite=dict(item)
        sql="INSERT INTO province.{} (".format(item.collection)
        v_list=[]
        k_list=[]
        for key,value in ite.items():
            if value !="None" and value !="":
                sql += "{},"
                v_list.append(ite[key])
                k_list.append(key)
        sql=sql.format(*k_list)[:-1]+")"+" VALUES ("
        for key,value in ite.items():
            if value !="None" and value !="":
                sql += "'{}',"
        sql=sql.format(*v_list)[:-1]+")"
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            try:
                self.db = psycopg2.connect(database=self.pgsql_db, user=self.pgsql_user, password=self.pgsql_pass,
                                           host=self.pgsql_uri, port=self.pgsql_port)
                self.cursor = self.db.cursor()
                self.cursor.execute(sql)
                self.db.commit()
            except:
                myclient = pymongo.MongoClient('mongodb://ecs-a025-0002:27017/')
                mydb=myclient[MONGODATABASE]
                mycol=mydb[MONGOTABLE]
                mydict = {"item":item,"reason":"写入数据库失败",'sql':sql,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                mycol.insert_one(mydict)
                myclient.close()
        return item

class ScrapyKafkaPipeline(object):
    def __init__(self):
        kafka_ip_port = BOOTSTRAP_SERVER
        # 初始化client
        self._client = KafkaClient(hosts=kafka_ip_port)
        # 初始化Producer 需要把topic name变成字节的形式
        self._producer = self._client.topics[TOPIC.encode(encoding="UTF-8")].get_producer()
    def process_item(self, item, spider):
        msg={
            "collection":item.collection,
            "content":dict(item)
        }
        try:
            self._producer.produce(json.dumps((msg),ensure_ascii=False).encode(encoding="UTF-8"))
        except (SocketDisconnectedError, LeaderNotAvailable) as e:
            try:
                self._producer = self._client.topics[TOPIC.encode(encoding="UTF-8")].get_producer()
                self._producer.stop()
                self._producer.start()
                self._producer.produce(json.dumps((msg),ensure_ascii=False).encode(encoding="UTF-8"))
            except Exception as e:
                myclient = pymongo.MongoClient('mongodb://ecs-a025-0002:27017/')
                mydb=myclient[MONGODATABASE]
                mycol=mydb[MONGOTABLE]
                mydict = {"item":msg,"reason":"写入kafka失败",'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                mycol.insert_one(mydict)
                myclient.close()
        return item
    def close_spider(self, spider):
        self._producer.stop()