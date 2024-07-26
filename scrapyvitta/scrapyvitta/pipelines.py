# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import shutil


class ScrapyvittaPipeline:
    def process_item(self, item, spider):
        return item


class MoveDbPipeline:
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        #movemos el archivo .db y .db-journal despúes de que el spider haya terminado
        directory = 'db'
        if not os.path.exists(directory):
            os.makedirs(directory)

        db_file = 'output.db'
        journal_file = f'{db_file}-journal'

        source_db_path = db_file
        source_journal_path = journal_file
        destination_db_path = os.path.join(directory, db_file)
        destination_journal_path = os.path.join(directory, journal_file)

        if os.path.exists(source_db_path):
            shutil.move(source_db_path, destination_db_path)
        if os.path.exists(source_journal_path):
            shutil.move(source_journal_path, destination_journal_path)