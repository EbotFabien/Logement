from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
from flask_cors import CORS,cross_origin



db_voie = db.collection('voie')

voie = Blueprint('voie',__name__)


@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@voie.route('/voie/ajouter', methods=['POST'])
def create():
    temps,res_= db_voie.add(request.json)
    todo = db_voie.document(res_.id).get()
    finzl_= todo.to_dict()
    finzl_['id_'] = res_.id
    return jsonify(finzl_), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@voie.route('/voie/tous', methods=['GET'])
def read():
    
    todo = db_voie.stream()
    final_ = []
    temp = {}
    for tod in todo:        
        temp = tod.to_dict()
        temp['_id'] = tod.id
        final_.append(temp)
    return jsonify(final_), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content-Type','Authorization'])
@voie.route('/voie/<int:ide>', methods=['GET'])
def read_ind(ide):


    todo_id = str(ide)
    
    if todo_id:
        todo = db_voie.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200


@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@voie.route('/voie/update/<int:ide>', methods=['POST', 'PUT'])
def update(ide):
        todo_id = str(ide)
        todo = db_voie.document(todo_id).get()
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            db_voie.document(todo_id).update(request.json)
            return jsonify({"success": True}), 200
        

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@voie.route('/voie/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    todo_id = str(ide)
    todo = db_voie.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'existe pas"}), 400
    else:
        db_voie.document(todo_id).delete()
        return jsonify({"success": True}), 200
    