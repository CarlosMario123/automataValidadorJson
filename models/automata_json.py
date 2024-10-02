class AutomataJSON:
    def __init__(self):
        self.estado_actual = 'q1'
        self.estados_aceptacion = {'terminated'}
        self.json_procesado = ""  
        self.json_validos = []  # Lista para almacenar los JSON válidos
        self.transition =   {          'q1': {
                " ": "q1", "\t": "q1", "\n": "q1",
                "{": "q2", 
            },
            'q2': {
                " ": "q2", "\t": "q2", "\n": "q2", 
                "}": "terminated",  
                '"': "q4", 
            },
            'terminated': {
                " ": "terminated", "\t": "terminated", "\n": "terminated"
            },  
            "q4": {  # Inicio de cadena para la clave
                **{chr(i): "q4.1" for i in range(32, 127)},
                '"': "q5",  # Fin de la clave
            },
            "q4.1": {  
                **{chr(i): "q4.1" for i in range(32, 127)},  # Permitir caracteres visibles ASCII
                '"': "q5",  # Fin de la clave
            },
            "q5": {  
                " ": "q5", "\t": "q5", "\n": "q5",  
                ":": "q6",
            },
            "q6": {  
                " ": "q6", "\t": "q6", "\n": "q6",  
                **{chr(i): "q7" for i in range(48, 58)},  # Números 0-9
                "t": "q12",  # Procesar 'true'
                "f": "q21",  # Procesar 'false'
                "n": "q25",  # Procesar 'null'
                '"': "q10",  # Procesar una cadena como valor
                "[": "q15",  # Procesar un array como valor
            },
            "q7": {  # Procesar número
                " ": "q7", "\t": "q7", "\n": "q7",  # Ignorar espacios dentro de números
                **{chr(i): "q7" for i in range(48, 58)},  # Números 0-9
                "}": "terminated",
                ".": "q8",  # Procesar números decimales
                ",": "q9",  # Procesar más valores
            },
            "q8": {  # Procesar decimales
                " ": "q8", "\t": "q8", "\n": "q8",  # Ignorar espacios después del punto decimal
                **{chr(i): "q8" for i in range(48, 58)},  # Números 0-9
                "}": "terminated",
                ",": "q9",  # Procesar más valores
            },
            "q9": {  # Procesar después de una coma
                " ": "q9", "\t": "q9", "\n": "q9",  # Ignorar espacios, tabulaciones y saltos de línea
                '"': "q4",  # Nueva clave
            },
            "q10": {  # Procesar cadenas dentro de valores
                **{chr(i): "q10" for i in range(32, 127)},  # Permitir cualquier carácter visible ASCII dentro de cadenas
                '"': "q11",  # Fin de la cadena
            },
            "q11": {  # Después de una cadena
                " ": "q11", "\t": "q11", "\n": "q11",  # Ignorar espacios
                "}": "terminated",
                ",": "q9",  
            },
            "q12": {  # Procesar 't' de 'true'
                "r": "q13",
            },
            "q13": {  # Procesar 'r' de 'true'
                "u": "q14"
            },
            "q14": {  
                "e": "q7",  
            },
            "q21": { 
                "a": "q22",
            },
            "q22": {  # Procesar 'a' de 'false'
                "l": "q23",
            },
            "q23": {  # Procesar 'l' de 'false'
                "s": "q24",
            },
            "q24": {  # Procesar 's' de 'false'
                "e": "q7",  
            },
            "q25": {  # Procesar 'n' de 'null'
                "u": "q26",
            },
            "q26": {  # Procesar 'u' de 'null'
                "l": "q27",
            },
            "q27": {  # Procesar 'l' de 'null'
                "l": "q7", 
            },
            "q15": {  # Procesar arrays
                " ": "q15", "\t": "q15", "\n": "q15",  # Ignorar espacios dentro del array
                **{chr(i): "q16" for i in range(48, 58)},  # Números 0-9
                '"': "q18",  # Procesar cadenas dentro del array
                "t": "q15.t1",  # Procesar 'true' en array
                "f": "q15.f1",  # Procesar 'false' en array
                "n": "q15.n1",  
                ",": "q15", 
                "]": "q20",  
            },
            "q16": {  # Procesar numeros dentro del array
                " ": "q16", "\t": "q16", "\n": "q16",  # Ignorar espacios dentro del array
                **{chr(i): "q16" for i in range(48, 58)},  # Números 0-9
                ".": "q17",  # Números decimales
                "]": "q20",  # Cierre del array
                ",": "q15",  
            },
            "q17": {  # Procesar números decimales dentro del array
                " ": "q17", "\t": "q17", "\n": "q17",  # Ignorar espacios
                **{chr(i): "q17" for i in range(48, 58)},  # Números 0-9
                "]": "q20",  # Cierre del array
                ",": "q15",  # Más elementos en el array
            },
            "q18": {  # Procesar cadenas dentro del array
                **{chr(i): "q18" for i in range(32, 127)},  # Permitir cualquier carácter visible ASCII
                '"': "q19",  # Fin de la cadena
            },
            "q19": { 
                " ": "q19", "\t": "q19", "\n": "q19", 
                ",": "q15",  # Más elementos en el array
                "]": "q20",  # Cierre del array
            },
            "q20": {  # Procesar cierre del array
                " ": "q20", "\t": "q20", "\n": "q20",  
                "}": "terminated",
                ",": "q9",  # Procesar más pares clave-valor después del array
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
