from flask import render_template, url_for,flash,redirect,request,abort,Blueprint,jsonify
from app import db,bcrypt
from flask_cors import CORS,cross_origin

db_cles = db.collection('cles')
db_client = db.collection('client')
db_compteur = db.collection('compteur')
db_extenssion= db.collection('extenssion')
db_piece= db.collection('piece')
db_rubriq= db.collection('rubriq')
db_user= db.collection('user')
db_voie= db.collection('voie')
db_logement= db.collection('logement')
db_type_log= db.collection('type_log')






logement = Blueprint('logement',__name__)

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@logement.route('/logement/ajouter', methods=['POST'])
def create():
    clefs ={}
    compteurs = {}
    pieces = {}
    rubriques ={}
    data_ = request.json
    type_logement = getDataByID(db_type_log,data_['type_log'])
    i = 0
    for val_ in type_logement['cles'].values():
        clefs["cles_"+str(i)] = getDataByID(db_cles,val_)
    type_logement['cles'] = clefs
    
    i = 0
    for val_ in type_logement['compteur'].values():
        compteurs["compteurs_"+str(i)] = getDataByID(db_compteur,val_)
    type_logement['compteur'] = compteurs
    
    i = 0
    for val_ in data_["piece"].values():
        pieces["piece"+str(i)] = getDataByID(db_piece,val_)
        i+=1
        
    i = 0
    for valeur in pieces.values():
        k=0
        for val1_ in valeur['rubriq'].values():
            rubriques["rubriq"+str(k)] = getDataByID(db_rubriq,val1_)
            k+=1
        valeur['rubriq'] = rubriques
        i+=1
    type_logement['piece'] = pieces
    
    data_['type_log'] = type_logement
    data_['extenssion'] = getDataByID(db_extenssion,data_['extenssion'])
    data_['voie'] = getDataByID(db_voie,data_['voie'])
    data_['client'] = getDataByID(db_client,data_['client'])
    data_.pop('piece')
    
    temps,res_= db_logement.add(data_)
    todo = db_logement.document(res_.id).get()
    finzl_= todo.to_dict()
    finzl_['id_'] = res_.id
    return jsonify(data_), 200
      


def getDataByID(bd,id):
    todo = bd.document(id).get()
    final_= todo.to_dict()
    final_['_id'] = id
    return final_

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@logement.route('/logement/tous', methods=['GET'])
def read():
    all_todos = [doc.to_dict() for doc in db_logement.stream()]
    return jsonify(all_todos), 200

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@logement.route('/logement/tous', methods=['GET'])
def read_all():
    todo = db_logement.stream()
    final_ = []
    temp = {}
    for tod in todo:
        temp = tod.to_dict()
        temp['_id'] = tod.id
        final_.append(temp)
    return jsonify(final_), 200
    

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@logement.route('/logement/<string:ide>', methods=['GET'])#hide data
def read_ind(ide):
    todo = db_logement.document(ide)
    final_={}
    if todo is None:
        return jsonify({"Fail": "donnee n'existe pas"}), 400
    else:
        final_= todo.get().to_dict()  
    final_["_id"] = ide
    return jsonify(final_), 200

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@logement.route('/logement/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
    todo = db_logement.document(ide)
    final_= {}
    if todo is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        todo.update(request.json)
        todo = db_logement.document(ide).get()
        final_= todo.to_dict()
    final_["_id"] = ide
    print(final_["_id"])
    return jsonify(final_), 200

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@logement.route('/logement/delete/<int:ide>', methods=['GET', 'DELETE'])
def delete(ide):
    print(ide)
    todo_id = str(ide)
    
    todo = db_logement.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        db_logement.document(todo_id).delete()
        return jsonify({"success": True}), 200