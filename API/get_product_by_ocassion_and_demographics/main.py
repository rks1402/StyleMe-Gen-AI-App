from google.cloud import datastore
datastore_client = datastore.Client()

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values...
    """
    gender=""
    query = datastore_client.query(kind='MasterData')
    request_json = request.get_json()

    if request_json and 'Occasion' in request_json:
        ocassion = request_json['Occasion']
        ocassion = ocassion.lower()
        query.add_filter('ocassion', '=', ocassion)
    else:
        return f'Data not found'

    request_json = request.get_json()
    if request_json and 'Demographics' in request_json:
        Demographics = request_json['Demographics']
        if 'gender' in 'Demographics':
            gender = Demographics['gender']
            gender = gender.lower()
            query.add_filter('gender', '=', gender)

    if request_json and 'color' in request_json:
        color = request_json['color']
        color = color.lower()
        query.add_filter('color', '=', color)

    if request_json and 'material' in request_json:
        material = request_json['material']
        material = material.lower()
        query.add_filter('material', '=', material)

    if request_json and 'pattern' in request_json:
        pattern = request_json['pattern']
        pattern = pattern.lower()
        query.add_filter('pattern', '=', pattern)

    results = query.fetch()
    l=list()
    for result in results:
        l.append(result['product_ID'])
    result=str(l)

    return result
