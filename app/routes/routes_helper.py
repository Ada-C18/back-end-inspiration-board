from flask import make_response, abort

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid, id must be a number"}, 400))
    
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"There is no existing {cls.__name__} {model_id}"}, 404))
    
    return model
