from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db
from bson import ObjectId
from bson.errors import InvalidId 
import uuid

items_bp = Blueprint('items', __name__, url_prefix='/items')

def serialize_item(item) -> dict:
   item['_id'] = str(item['_id'])
   return item

def valid_object_id(id):
    try:
        return ObjectId(id)
    except InvalidId:
        return None

@items_bp.get('/')
@jwt_required()
def get_all():
    db = get_db()
    items = list(db.animals.find())
    return jsonify([serialize_item(i) for i in items]), 200

@items_bp.post('/')
@jwt_required()
def create():
    data = request.get_json()
    Age = data.get('Age_Upon_Outcome')
    Animal_Type = data.get('Animal_Type')
    Gender = data.get('Gender')
    name = data.get('Name')
    Date_of_Birth = data.get('Date_of_Birth')
    

    if not Age or not Animal_Type or not Gender or not name or not Date_of_Birth:
        return jsonify({"error": "Required fields are missing"}), 400

    db = get_db()

    last_animal = db.animals.find_one(sort=[("id", -1)])
    next_id = str(int(last_animal['id']) + 1) if last_animal else "1"

    result = db.animals.insert_one({
        "id": next_id,
        "Age_Upon_Outcome": Age,
        "Animal_ID": str(uuid.uuid4()),
        "Animal_Type": Animal_Type,
        "Gender": Gender,
        "Name": name,
        "Date_of_Birth": Date_of_Birth
    })
    new_item = db.animals.find_one({"_id": result.inserted_id})
    return jsonify(serialize_item(new_item)), 201


@items_bp.put('/<id>')
@jwt_required()
def update(id):
    oid = valid_object_id(id)
    if not oid:
        return jsonify({"error": "Invalid ID format"}), 400 

    data = request.get_json()
    name = data.get('Name')
    Animal_Type = data.get('Animal_Type')

    if not name and not Animal_Type:
        return jsonify({"error": "At least one field (name or Animal_Type) is required"}), 400

    db = get_db()
    item = db.animals.find_one({"_id": oid})
    if not item:
        return jsonify({"error": "Item not found"}), 404

    update_data = {}
    if name:
        update_data['name'] = name
    if Animal_Type:
        update_data['Animal_Type'] = Animal_Type

    db.animals.update_one({"_id": oid}, {"$set": update_data})
    updated_item = db.animals.find_one({"_id": oid})
    return jsonify(serialize_item(updated_item)), 200

@items_bp.delete('/<id>')
@jwt_required()
def delete(id):
    oid = valid_object_id(id)
    if not oid:
        return jsonify({"error": "Invalid ID format"}), 400 

    db = get_db()
    result = db.animals.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Item deleted successfully"}), 200
