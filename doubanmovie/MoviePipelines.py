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
                print("Repetition Data!")
                pass

            else:
                self.cursor.execute(
                    """insert into doubanmovie(name, info, rating, num, quote, img_url) value (%s, %s, %s, %s, %s, %s)""",
                    (item['name'],
                     item['info'],
                     item['rating'],
                     item['num'],
                     item['quote'],
                     item['img_url']))
                self.connect.commit()

        except Exception as error:
            # 打印详细错误信息，使用logging.error函数
            logging.error(error, exc_info=True)
            print('未成功写入')
            pass

        return item


