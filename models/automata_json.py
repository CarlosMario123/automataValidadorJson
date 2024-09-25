import csv

class AutomataJSON:
    def __init__(self):
        self.estado_actual = 'q1'
        self.estados_aceptacion = {'terminated'}
        self.errores = []
        self.fila = 1
        self.columna = 1
        self.transition = {
            'q1': {
                "{": "q2"
            },
            'q2': {
                "}": "terminated",
                '"': "q4",
            },
            'terminated': {  # Estado de aceptación
            },
            "q4": {
                **{chr(i): "q4" for i in range(48, 58)},  # Números 0-9
                **{chr(i): "q4" for i in range(97, 123)},  # Letras a-z
                **{chr(i): "q4" for i in range(65, 91)},  # Letras A-Z
                '"': "q5",
            },
            "q5": {
                ':': "q6",
            },
            "q6": {
                **{chr(i): "q7" for i in range(48, 58)},  # Números 0-9
                "t": "q12",  # Procesa 'true'
                "f": "q21",  # Procesa 'false'
                "n": "q25",  # Procesa 'null'
                '"': "q10",
                "[": "q15",
            },
            "q7": {
                **{chr(i): "q7" for i in range(48, 58)},  # Números 0-9
                "}": "terminated",
                ".": "q8",
                ",": "q9",
            },
            "q8": {
                **{chr(i): "q8" for i in range(48, 58)},  # Números 0-9
                "}": "terminated",
                ",": "q9",
            },
            "q9": {
                '"': "q4"
            },
            "q10": {
                **{chr(i): "q10" for i in range(48, 58)},  # Números 0-9
                **{chr(i): "q10" for i in range(97, 123)},  # Letras a-z
                **{chr(i): "q10" for i in range(65, 91)},  # Letras A-Z
                '"': "q11",
            },
            "q11": {
                "}": "terminated",
                ",": "q9",
            },
            "q12": {  # Procesa 't' de true
                "r": "q13",
            },
            "q13": {  # Procesa 'r' de true
                "u": "q14"
            },
            "q14": {  # Procesa 'u' de true
                "e": "q7",  # Fin de 'true'
            },
            "q21": {  # Procesa 'f' de false
                "a": "q22",
            },
            "q22": {  # Procesa 'a' de false
                "l": "q23",
            },
            "q23": {  # Procesa 'l' de false
                "s": "q24",
            },
            "q24": {  # Procesa 's' de false
                "e": "q7",  # Fin de 'false'
            },
            "q25": {  # Procesa 'n' de null
                "u": "q26",
            },
            "q26": {  # Procesa 'u' de null
                "l": "q27",
            },
            "q27": {  # Procesa 'l' de null
                "l": "q7",  # Fin de 'null'
            },
            "q15": {  # Estado que procesa el inicio de un array [
                **{chr(i): "q16" for i in range(48, 58)},  # Números 0-9
                '"': "q18",  # Cadenas
                "t": "q15.t1",  # Procesar 'true' en array
                "f": "q15.f1",  # Procesar 'false' en array
                "n": "q15.n1",  # Procesar 'null' en array
            },
            "q15.t1": {  # Procesa 't' de true dentro del array
                "r": "q15.t2"
            },
            "q15.t2": {  # Procesa 'r' de true dentro del array
                "u": "q15.t3"
            },
            "q15.t3": {  # Procesa 'u' de true dentro del array
                "e": "q15.t5"
            },
            "q15.t5": {  # Después de 'true' en array
                "]": "q20",  # Cierra el array
                ",": "q15",  # Más elementos en el array
            },
            "q15.f1": {  # Procesa 'f' de false dentro del array
                "a": "q15.f2"
            },
            "q15.f2": {  # Procesa 'a' de false dentro del array
                "l": "q15.f3"
            },
            "q15.f3": {  # Procesa 'l' de false dentro del array
                "s": "q15.f4"
            },
            "q15.f4": {  # Procesa 's' de false dentro del array
                "e": "q15.t5"  # Fin de 'false', se comparte con 'true'
            },
            "q15.n1": {  # Procesa 'n' de null dentro del array
                "u": "q15.n2"
            },
            "q15.n2": {  # Procesa 'u' de null dentro del array
                "l": "q15.n3"
            },
            "q15.n3": {  # Procesa 'l' de null dentro del array
                "l": "q15.t5"  # Fin de 'null', se comparte con 'true' y 'false'
            },
            "q16": {  # Procesa números dentro del array
                **{chr(i): "q16" for i in range(48, 58)},  # Números 0-9
                ".": "q17",  # Números decimales
                "]": "q20",  # Cierre del array
                ",": "q15",  # Más elementos en el array
            },
            "q17": {  # Procesa números decimales dentro del array
                **{chr(i): "q17" for i in range(48, 58)},  # Números 0-9
                "]": "q20",  # Cierre del array
                ",": "q15",  # Más elementos en el array
            },
            "q18": {  # Procesa cadenas dentro del array
                **{chr(i): "q18" for i in range(48, 58)},  # Números 0-9
                **{chr(i): "q18" for i in range(97, 123)},  # Letras a-z
                **{chr(i): "q18" for i in range(65, 91)},  # Letras A-Z
                '"': "q19",  # Fin de la cadena
            },
            "q19": {  # Después de cadena en array
                ",": "q15",  # Más elementos en el array
                "]": "q20",  # Cierra el array
            },
            "q20": {  # Procesa el cierre del array
                "}": "terminated",
                ",": "q9",  # Procesa más pares clave-valor después del array
            },
        }

    def procesar_json(self, texto_json):
        self.fila = 1
        self.columna = 1
        self.errores.clear()
        self.estado_actual = 'q1'
        
        for caracter in texto_json:
            if caracter in [' ', '\t', '\n']: 
                if caracter == '\n':
                    self.fila += 1
                    self.columna = 1
                else:
                    self.columna += 1
                continue
            
            try:
                self.procesar_caracter(caracter)
            except ValueError as e:
                print(e)
                return False
        
        return self.estado_actual in self.estados_aceptacion

    def procesar_caracter(self, caracter):
        if caracter in self.transition.get(self.estado_actual, {}):
            self.estado_actual = self.transition[self.estado_actual][caracter]
        else:
            self.reportar_error(f"Carácter inesperado: '{caracter}'")

    def reportar_errores_csv(self, ruta_csv):
        with open(ruta_csv, mode='w', newline='', encoding='utf-8') as archivo_csv:
            escritor_csv = csv.DictWriter(archivo_csv, fieldnames=['error', 'fila', 'columna'])
            escritor_csv.writeheader()
            escritor_csv.writerows(self.errores)

    def reportar_error(self, mensaje):
        error = f"{mensaje} en la fila {self.fila}, columna {self.columna}"
        self.errores.append({'error': mensaje, 'fila': self.fila, 'columna': self.columna})
        raise ValueError(error)
