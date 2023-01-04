from flask import jsonify, abort, make_response

def validate(cls,obj_id):
    try:
        obj_id = int(obj_id)
    except ValueError:
        response_str = f"details: invalid data"
        abort(make_response(jsonify({"message":response_str}), 400))

    matching_obj = cls.query.get(obj_id)

    if not matching_obj:
        response_str = f"{cls.__name__.lower()} not found"
        abort(make_response(jsonify({"message":response_str}), 404))

    return matching_obj