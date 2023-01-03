from app import db
from flask import abort, make_response, jsonify

def validate_model(class_obj, object_id):
    try:
        object_id = int(object_id)
    except:
        abort(make_response(jsonify({"message": f"{class_obj.__name__} {object_id} has an invalid id"}), 400))

    query_result = class_obj.query.get(object_id)

    if not query_result:
        abort(make_response({"message": f"{class_obj.__name__} {object_id} not found"}, 404))

    return query_result
