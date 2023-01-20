from flask import jsonify, abort, make_response

def get_one_obj_or_abort(cls, obj_id):
    try:
        obj_id = int(obj_id)
    except ValueError:
        response_str = f"Invalid ID: `{obj_id}`. ID must be an integer"
        abort(make_response(jsonify({"message":response_str}), 400))

    matching_obj = cls.query.get(obj_id)

    if not matching_obj:
        return abort(make_response({"message": f"{cls.__name__} {obj_id} not found"}, 404))

    return matching_obj