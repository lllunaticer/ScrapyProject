# -*- coding: utf-8 -*-

import json
import io
import pymysql
from doubanmovie import settings
import logging



class MoviePipeline(object):
    def __init__(self):
        self.file = io.open('data.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False)+"\n"
        self.file.write(line)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.file.close()


class DBPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=3306,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """select * from doubanmovie where img_url = %s""",
                item['img_url'])
            repetition = self.cursor.fetchone()

            if repetition:
                pass

            else:
                self.cursor.excute(
                    """insert into doubanmovie(name, info, rating, num, quote, img_url) value (%s, %s, %s, %s, %s, %s)""",
                    (item['name'],
                     item['info'],
                     item['rating'],
                     item['num'],
                     item['quote'],
                     item['img_url']))

                self.connect.commit()

        except Exception as error:
            logging.log(error)

        return item


