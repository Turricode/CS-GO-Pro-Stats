from pymongo import MongoClient
import os

client = MongoClient(os.environ['DB_CONNECT'])

db = client['Stats']

teams_collection = db['Teams']
players_collection = db['Players']  