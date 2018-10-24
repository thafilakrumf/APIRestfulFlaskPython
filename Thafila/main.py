from flask import Flask, jsonify, request
from client import Client
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://172.18.0.35:27017/DBthafila"
mongo = PyMongo(app)

#listClients =[
 #   Client(name="Zezinho", email="ze@univille.br", phone="5551234"),
  #  Client(name="Luizinho", email="lu@univille.br", phone="5555432"),
   # Client(name="Huguinho", email="hu@univille.br", phone="5556666"),
#]

@app.route('/api/v1.0/clients', methods=['GET'])
def get_tasks():
    clients = []
    for c in mongo.db.clients.find():
        newClient = Client()
        newClient._id = str(c['_id'])
        newClient.name = c['name']
        newClient.phone = c['phone']
        newClient.email = c['email']
        clients.append(newClient)

    return jsonify([c.__dict__ for c in clients]),201

@app.route('/api/v1.0/clients', methods=['POST'])
def create_client():
    newcli = Client()
    newcli._id = ObjectId()
    newcli.name = request.json['name']
    newcli.email = request.json['email']
    newcli.phone = request.json['phone']

    ret = mongo.db.clients.insert_one(newcli.__dict__).inserted_id
    return jsonify({'id': str(ret)}),201

@app.route('/api/v1.0/clients/<string:_id>', methods=["PUT"])
def update_client(_id):
    updatecli = Client()
    updatecli._id = ObjectId(_id)
    updatecli.name = request.json['name']
    updatecli.email = request.json['email']
    updatecli.phone = request.json['phone']
    mongo.db.clients.update_one({'_id':updatecli._id}, \
                                {'$set':updatecli.__dict__}, \
                                upsert=False)
    return jsonify({'id':str(updatecli._id)}),201

@app.route('/api/v1.0/clients/<string:_id>', methods=['DELETE'])
def delete_client(_id):
    _id = ObjectId(_id)
    ret = mongo.db.clients.delete_one({'_id':_id}).deleted_count
    return jsonify({'delete_count': str(ret)}),201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)







