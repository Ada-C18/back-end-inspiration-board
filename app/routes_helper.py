from flask import jsonify, abort, make_response

def get_one_obj_or_abort(cls, obj_id):
    try:
        obj_id = int(obj_id)
    except ValueError:
        response_str = f"Invalid ID: `{obj_id}`. ID must be an integer"
        abort(make_response(jsonify({"message":response_str}), 400))
    
    matching_obj = cls.query.get(obj_id)

    if not matching_obj:
        response_str = f"{cls.__name__} with id `{obj_id}` was not found in the database."
        abort(make_response(jsonify({"message":response_str}), 404))
    
    return matching_obj