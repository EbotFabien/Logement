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
    
    """temps,res_= db_logement.add(data_)
    todo = db_logement.document(res_.id).get()
    finzl_= todo.to_dict()
    finzl_['id_'] = res_.id"""
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
    all_logement = [doc.to_dict() for doc in db_logement.stream()]
    all_cles = [doc.to_dict() for doc in db_cles.stream()]
    all_client = [doc.to_dict() for doc in db_client.stream()]
    all_compteur = [doc.to_dict() for doc in db_compteur.stream()]
    all_extension = [doc.to_dict() for doc in db_extenssion.stream()]
    all_rubriq = [doc.to_dict() for doc in db_rubriq.stream()]
    all_piece = [doc.to_dict() for doc in db_piece.stream()]
    all_user = [doc.to_dict() for doc in db_user.stream()]
    all_voie = [doc.to_dict() for doc in db_voie.stream()]
     
     
     
     
    return jsonify({"logement": all_logement,
        "cles": all_cles,
        "client": all_client,
        "compteur": all_compteur,
        "extenssion" : all_extension,
        "rubriq" : all_rubriq,
        "piece" : all_piece,
        "user" : all_user,
        "voie" : all_voie
        }), 200
    

@cross_origin(origin=["http://127.0.0.1","http://195.15.228.250","*"],headers=['Content- Type','Authorization'])
@logement.route('/logement/<string:ide>', methods=['GET'])#hide data
def read_ind(ide):
    todo = db_logement.document(ide).get()
    final_= todo.to_dict()
    final_
    clefs = {}
    pieces = {}
    rubriqs = {}
    clients = {}
    compteurs = {}
    extenssions ={}
    type_logs= {}
    voies = {}
    
    
    i = 0
    for val_ in final_["cles"].values():
        clefs["cles"+str(i)] = getDataByID(db_cles,val_)
        i+=1
    
    i = 0
    for val_ in final_["client"].values():
        clients["clients"+str(i)] = getDataByID(db_client,val_)
        i+=1
    
    i = 0
    for val_ in final_["compteur"].values():
        compteurs["compteurs"+str(i)] = getDataByID(db_compteur,val_)
        i+=1
        
    i = 0
    for val_ in final_["extenssion"].values():
        extenssions["extenssions"+str(i)] = getDataByID(db_extenssion,val_)
        i+=1
        
    i = 0
    for val_ in final_["piece"].values():
        pieces["piece"+str(i)] = getDataByID(db_piece,val_)
        i+=1
        
    i = 0
    for valeur in pieces.values():
        k=0
        for val1_ in valeur['rubriq'].values():
            rubriqs["rubriq"+str(k)] = getDataByID(db_rubriq,val1_)
            k+=1
        valeur['rubriq'] = rubriqs
        i+=1
    
   
   
         
    """i = 0
    for val4_ in final_["extenssion"].values():
        extenssion = db_extenssion.document(val4_).get().to_dict()
        extenssion["_id"] = val4_
        extenssions["extenssion"+str(i)] = extenssion
        i+=1
   
    i = 0
   
    for val5_ in final_["type_log"].values():
        type_log = db_type_log.document(val5_).get().to_dict()
        type_log["_id"] = val5_
        k=0
        for val5_1 in type_log['cles'].values():
            cles= db_cles.document(val5_1).get().to_dict()
            cles['_id']=val5_1
            clefs["cles"+str(k)]=cles
            k+=1
       
     #   type_logs["type_log"+str(i)] = type_log
        
        #i+=1
        
    i = 0
    for val3_ in final_["compteur"].values():
        compteur = db_compteur.document(val3_).get().to_dict()
        compteur["_id"] = val3_
        compteurs["compteur"+str(i)] = compteur
        i+=1
        
    i = 0
    for val2_ in final_["client"].values():
        client = db_client.document(val2_).get().to_dict()
        client["_id"] = val2_
        clients["client"+str(i)] = client
        i+=1
        
    i = 0
    for val_ in final_['piece'].values():
        piece = db_piece.document(val_).get().to_dict()
       
        piece["_id"] = val_
        print(piece["rubriq"])
        k = 0
        for val1_ in piece['rubriq'].values():
             rubriq = db_rubriq.document(val1_).get().to_dict()
             rubriq["_id"] = val1_
             rubriqs["rubrique"+str(k)] = rubriq
             k+=1
        pieces["piece"+str(i)] = piece
        
       # for val1_ in pieces["piece"+str(i)].values():
        
    final_['cles'] = clefs
    final_['pieces'] = pieces
    final_['client'] = clients
    final_['compteur'] =compteurs
    final_['extenssion'] =extenssions
    final_['type_log'] = type_logs
    final_['voie'] = voies"""
    final_['cles'] = clefs
    final_['client'] = clients
    final_['compteur'] = compteurs
    final_["extenssion"] = extenssions
    final_["piece"] = pieces
    
    return jsonify(final_),200
    
    if todo_id:
        todo = db_logement.where('email','==',todo_id)
        if todo.to_dict() is None:
            return jsonify({"Fail": "donnee n'exist pas"}), 400
        else:
            return jsonify(todo.to_dict()), 200

@cross_origin(origin=["http://127.0.0.1:5274","http://195.15.228.250","*"],headers=['Content-Type','Authorization'],automatic_options=False)
@logement.route('/logement/update/<ide>', methods=['POST', 'PUT'])
def update(ide):
   
        todo = db_logement.document(ide)
        
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
    todo_id = str(ide)
    todo = db_logement.document(todo_id).get()
    if todo.to_dict() is None:
        return jsonify({"Fail": "donnee n'exist pas"}), 400
    else:
        db_logement.document(todo_id).delete()
        return jsonify({"success": True}), 200