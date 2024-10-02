import json

def formatear_json(json_string):
    try:

        data = json.loads(json_string)
        json_formateado = json.dumps(data, indent=4)
        
        return json_formateado

    except json.JSONDecodeError:
        return "El formato del JSON es inválido."

def arrayToJsonFormated(array):
    newArray = []
    for i in array:
        newArray.append(formatear_json(i))
    return newArray

