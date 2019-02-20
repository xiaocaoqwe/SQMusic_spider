# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests, os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Index

from .items import SqmusicItem, SQmusicItem

engine = create_engine("mysql+pymysql://root:xiao12138@localhost/me", encoding='utf-8')
Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    category = Column(String(64))


class Singer(Base):
    __tablename__ = 'singer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    nid = Column(Integer, ForeignKey("category.id"))


class Infos(Base):
    __tablename__ = 'info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    song = Column(String(64))
    size = Column(String(64))
    link = Column(String(256))
    sid = Column(Integer, ForeignKey("singer.id"))


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.add_all([
    Category(category='华语男歌手'),
    Category(category='华语女歌手'),
    Category(category='华语乐队'),
    Category(category='专辑'),
    Category(category='欧美歌手'),
])
session.commit()


class SqmusicPipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, SqmusicItem):
            singers = dict(item)
            obj = Singer(name=singers['name'][0], nid=singers['category'])
            session.add(obj)
            session.commit()
            img = requests.get('https://www.sq688.com{}'.format(singers['name'][1])).content
            if os.path.exists('D:/Python/my project/Django框架/SQMusic/static/images/{}.jpg'.format(singers['name'][0])):
                pass
            else:
                with open('D:/Python/my project/Django框架/SQMusic/static/images/{}.jpg'.format(singers['name'][0]), 'wb') as f:
                    f.write(img)

        elif isinstance(item, SQmusicItem):
            info = dict(item)
            data = session.query(Singer).filter_by(name=info['infos'][0]).first()
            ob = Infos(song=info['infos'][1], size=info['infos'][2], link=info['infos'][3], sid=data.id)
            session.add(ob)
            session.commit()
        return item
