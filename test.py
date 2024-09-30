from models.automata_json import AutomataJSON


def test_automata_json():
    # Inicializar el autómata
    automata = AutomataJSON()
    
    # Caso 1: Un JSON válido
    texto_json1 = 'a{"name":"Carlos","edad":15}aaa{"name":[1,2]}aw{"boolean":false},,{"name":1}'
    
    try:
        automata.procesar_json(texto_json1)
        print("Caso 1: El archivo JSON es correcto")
        print(automata.json_validos)
    except Exception as e:
        print(e)
  

test_automata_json()