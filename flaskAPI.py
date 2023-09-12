from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
parser = reqparse.RequestParser()
class PropertyData(db.Model):
    
    __tablename__ = 'scrapped_data'
    doc_no = db.Column(db.Text, primary_key=True)
    doc_type = db.Column(db.Text)
    office_circle = db.Column(db.Text)
    year = db.Column(db.Text)
    buyer_name = db.Column(db.Text)
    seller_name = db.Column(db.Text)
    other_info = db.Column(db.Text)
    doc_link =db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.doc_no}>'


'''
Query Params
name

Search will work on buyer name as well as sellter name

search

It works searching on Other Infrotmations column
'''

class ListPropertyData(Resource):
  
    def get(self):

        args = request.args
        name = args.get('name')
        search = args.get('search')

        # Query PropertyData and filter by buyer_name if provided
        query = PropertyData.query
        if name:
            query = query.filter(PropertyData.buyer_name.ilike(f'%{name}%') | 
                (PropertyData.seller_name.ilike(f'%{name}%'))
                )
        if search:
            query = query.filter(PropertyData.other_info.ilike(f'%{search}%'))
        data = query.all()
        

        # Create a list of dictionaries for JSON serialization
        data_list = [{'doc_no': item.doc_no,
                      'doc_type': item.doc_type,
                      'office_circle': item.office_circle,
                      'year': item.year,
                      'buyer_name': item.buyer_name,
                      'seller_name': item.seller_name,
                      'other_info': item.other_info,
                      'doc_link': item.doc_link} for item in data]

        return jsonify({'response': data_list})
    

class ListPropertyDataOnDocNumber(Resource):
  
    def get(self,doc_number):
        query = PropertyData.query
        query = query.filter(PropertyData.doc_no.ilike(f'%{doc_number}%'))
        data = query.all()
        

        # Create a list of dictionaries for JSON serialization
        data_list = [{'doc_no': item.doc_no,
                      'doc_type': item.doc_type,
                      'office_circle': item.office_circle,
                      'year': item.year,
                      'buyer_name': item.buyer_name,
                      'seller_name': item.seller_name,
                      'other_info': item.other_info,
                      'doc_link': item.doc_link} for item in data]

        return jsonify({'response': data_list})
    
class ListPropertyDataOnYear(Resource):
  
    def get(self,year):
        query = PropertyData.query
        query = query.filter(PropertyData.year.ilike(f'%{year}%'))
        data = query.all()
        

        # Create a list of dictionaries for JSON serialization
        data_list = [{'doc_no': item.doc_no,
                      'doc_type': item.doc_type,
                      'office_circle': item.office_circle,
                      'year': item.year,
                      'buyer_name': item.buyer_name,
                      'seller_name': item.seller_name,
                      'other_info': item.other_info,
                      'doc_link': item.doc_link} for item in data]

        return jsonify({'response': data_list})


  
  
  

api.add_resource(ListPropertyData, '/')
api.add_resource(ListPropertyDataOnDocNumber, '/doc/<int:doc_number>')
api.add_resource(ListPropertyDataOnYear, '/year/<int:year>')
  
  
# driver function
if __name__ == "__main__":
    app.run(port=8000, debug=True)
