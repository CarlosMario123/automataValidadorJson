class AutomataJSON:
    def __init__(self):
        self.estado_actual = 'q1'
        self.estados_aceptacion = {'terminated'}
        self.json_procesado = ""  
        self.json_validos = []  # Lista para almacenar los JSON válidos
        self.transition = {
            'q1': {
                " ": "q1", "\t": "q1", "\n": "q1",
                "{": "q2",  # Detecta inicio de JSON
            },
            'q2': {
                " ": "q2", "\t": "q2", "\n": "q2", 
                "}": "terminated",  # Detecta fin de JSON
                '"': "q4",  # Procesa claves (inicio de string)
                "[": "q15",  # Procesa arreglos dentro del JSON
            },
            'terminated': {
                " ": "terminated", "\t": "terminated", "\n": "terminated"
            },
            "q4": { 
                **{chr(i): "q4.1" for i in range(32, 127)},
                '"': "q5",  # Fin de la clave
            },
            "q4.1": {  # Permitir caracteres visibles ASCII en strings
                **{chr(i): "q4.1" for i in range(32, 127)},
                '"': "q5",  # Fin de la clave
            },
            "q5": {  # Después de una clave
                " ": "q5", "\t": "q5", "\n": "q5",
                ":": "q6",
            },
            "q6": {  # Procesar el valor después de dos puntos
                " ": "q6", "\t": "q6", "\n": "q6",
                **{chr(i): "q7" for i in range(48, 58)},  # Numeros 0-9
                '"': "q10",  # Procesar una cadena como valor
                "[": "q15",  # Procesar un array como valor
                "t": "q12",  # Procesar el valor booleano 'true'
                "f": "q21",  # Procesar el valor booleano 'false'
            },
            "q7": {  # Procesar números
                " ": "q7", "\t": "q7", "\n": "q7",
                **{chr(i): "q7" for i in range(48, 58)},  # Números 0-9
                "}": "terminated",  # Fin del objeto JSON
                "]": "q20",  # Fin del arreglo dentro del JSON
                ",": "q9",  # Más pares clave-valor
            },
            "q9": {  # Después de una coma
                " ": "q9", "\t": "q9", "\n": "q9",
                '"': "q4",  # Nueva clave
                "[": "q15",  # Nuevo array
            },
            "q10": {  # Procesar cadenas dentro de valores
                **{chr(i): "q10" for i in range(32, 127)},  # Permitir caracteres visibles ASCII en strings
                '"': "q11",  # Fin de la cadena
            },
            "q11": {  # Después de una cadena
                " ": "q11", "\t": "q11", "\n": "q11",
                "}": "terminated",  # Fin del objeto JSON
                ",": "q9",  # Más pares clave-valor
            },
            # Procesar booleano 'true'
            "q12": {  # 't'
                "r": "q13",  # 'tr'
            },
            "q13": {  # 'tr'
                "u": "q14",  # 'tru'
            },
            "q14": {  # 'tru'
                "e": "q7",  # 'true'
            },
            # Procesar booleano 'false'
            "q21": {  # 'f'
                "a": "q22",  # 'fa'
            },
            "q22": {  # 'fa'
                "l": "q23",  # 'fal'
            },
            "q23": {  # 'fal'
                "s": "q24",  # 'fals'
            },
            "q24": {  # 'fals'
                "e": "q7",  # 'false'
            },
            # Manejo de arreglos
            "q15": {  # Inicio del array
                " ": "q15", "\t": "q15", "\n": "q15",
                **{chr(i): "q16" for i in range(48, 58)},  # Números en el array
                "]": "q20",  # Cierre del array
            },
            "q16": {  # Procesar números dentro del array
                " ": "q16", "\t": "q16", "\n": "q16",
                **{chr(i): "q16" for i in range(48, 58)},  # Números en el array
                "]": "q20",  # Cierre del array
                ",": "q15",  # Más elementos en el array
            },
            "q20": {  # Después del cierre del array
                " ": "q20", "\t": "q20", "\n": "q20",
                "}": "terminated",  # Fin del objeto JSON
                ",": "q9",  # Más pares clave-valor
            },
        }

    def procesar_json(self, texto_json):
        self.json_procesado = ""  
        self.estado_actual = 'q1'
        
        for caracter in texto_json:
            try:
                self.procesar_caracter(caracter)
                self.json_procesado += caracter
                
                # Si el estado es 'terminated', se ha encontrado un JSON completo
                if self.estado_actual == 'terminated':  
                    self.json_validos.append(self.json_procesado.strip())  # Almacenar el JSON válido
                    self.json_procesado = ""  # Reiniciar para buscar otro JSON
                    self.estado_actual = 'q1'  # Reiniciar el autómata para seguir buscando
            except ValueError as e:
                # Reiniciar el autómata y continuar buscando
                self.json_procesado = ""  
                self.estado_actual = 'q1'

        return self.json_validos

    def procesar_caracter(self, caracter):
        if caracter in self.transition.get(self.estado_actual, {}):
            self.estado_actual = self.transition[self.estado_actual][caracter]
        else:
            raise ValueError(f"Carácter inesperado: '{caracter}'")

    def obtener_json_validos(self):
        return self.json_validos
