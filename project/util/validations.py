def validate_request(request):
    funcs = [
        validate_empty_request,
        validate_request_fields
    ]
    for func in funcs:
        validate, msg = func(request)
        if not validate:
            return validate, msg

    return True, 'OK'

def validate_empty_request(request):
    if not request.json:
        return False, 'Empty request'

    return True, 'OK'


def validate_request_fields(request):
    if not request.json['type']:
        return False, 'No type found'
    
    if not request.json['msg']:
        return False, 'No msg found'

    if not request.json['route']:
        return False, 'No route found'
 
    return True, 'OK'
