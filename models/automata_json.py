import csv

class AutomataJSON:
    def __init__(self):
        self.estado_actual = 'INICIO'
        self.estados_aceptacion = {'OBJETO_VALIDO', 'ARRAY_VALIDO'}
        self.errores = []
        self.fila = 1
        self.columna = 1

        self.transiciones = {
            'INICIO': {
                '{': 'ESPERA_LLAVE_O_FIN_OBJETO',
                '[': 'ESPERA_VALOR_O_FIN_ARRAY'
            },
            'ESPERA_LLAVE_O_FIN_OBJETO': {
                '"': 'LEYENDO_LLAVE',
                '}': 'OBJETO_VALIDO'
            },
            'LEYENDO_LLAVE': {
                'caracter': 'LEYENDO_LLAVE',  
                '"': 'DOS_PUNTOS'
            },
            'DOS_PUNTOS': {
                ':': 'ESPERA_VALOR'
            },
            'ESPERA_VALOR': {
                ' ': 'ESPERA_VALOR',
                '"': 'VALOR_CADENA',
                '{': 'ESPERA_LLAVE_O_FIN_OBJETO',
                '[': 'ESPERA_VALOR_O_FIN_ARRAY',
                't': 'PROCESANDO_TRUE_T',
                'f': 'PROCESANDO_FALSE_F',
                'n': 'PROCESANDO_NULL_N',
                '-': 'PROCESANDO_NUMERO',
                '0': 'PROCESANDO_NUMERO',
                '1': 'PROCESANDO_NUMERO',
                '2': 'PROCESANDO_NUMERO',
                '3': 'PROCESANDO_NUMERO',
                '4': 'PROCESANDO_NUMERO',
                '5': 'PROCESANDO_NUMERO',
                '6': 'PROCESANDO_NUMERO',
                '7': 'PROCESANDO_NUMERO',
                '8': 'PROCESANDO_NUMERO',
                '9': 'PROCESANDO_NUMERO'
            },
            'VALOR_CADENA': {
                'caracter': 'VALOR_CADENA',
                '"': 'ESPERA_COMA_O_FIN_OBJETO'  
            },
            'ESPERA_COMA_O_FIN_OBJETO': {
                ',': 'ESPERA_LLAVE_O_FIN_OBJETO',
                '}': 'OBJETO_VALIDO',
                ']': 'ARRAY_VALIDO',
                '"': 'LEYENDO_LLAVE',
                ' ': 'ESPERA_COMA_O_FIN_OBJETO'
            },
            'ESPERA_VALOR_O_FIN_ARRAY': {
                ']': 'ARRAY_VALIDO',
                ',': 'ESPERA_VALOR',
                ' ': 'ESPERA_VALOR_O_FIN_ARRAY'
            },
            'PROCESANDO_TRUE_T': {'r': 'PROCESANDO_TRUE_R'},
            'PROCESANDO_TRUE_R': {'u': 'PROCESANDO_TRUE_U'},
            'PROCESANDO_TRUE_U': {'e': 'ESPERA_COMA_O_FIN_OBJETO'},
            'PROCESANDO_FALSE_F': {'a': 'PROCESANDO_FALSE_A'},
            'PROCESANDO_FALSE_A': {'l': 'PROCESANDO_FALSE_L'},
            'PROCESANDO_FALSE_L': {'s': 'PROCESANDO_FALSE_S'},
            'PROCESANDO_FALSE_S': {'e': 'ESPERA_COMA_O_FIN_OBJETO'},
            'PROCESANDO_NULL_N': {'u': 'PROCESANDO_NULL_U'},
            'PROCESANDO_NULL_U': {'l': 'PROCESANDO_NULL_L1'},
            'PROCESANDO_NULL_L1': {'l': 'ESPERA_COMA_O_FIN_OBJETO'},
            'PROCESANDO_NUMERO': {
                '0': 'PROCESANDO_NUMERO',
                '1': 'PROCESANDO_NUMERO',
                '2': 'PROCESANDO_NUMERO',
                '3': 'PROCESANDO_NUMERO',
                '4': 'PROCESANDO_NUMERO',
                '5': 'PROCESANDO_NUMERO',
                '6': 'PROCESANDO_NUMERO',
                '7': 'PROCESANDO_NUMERO',
                '8': 'PROCESANDO_NUMERO',
                '9': 'PROCESANDO_NUMERO',
                '.': 'PROCESANDO_DECIMAL',
                ',': 'ESPERA_COMA_O_FIN_OBJETO',
                '}': 'OBJETO_VALIDO',
                ']': 'ARRAY_VALIDO'
            },
            'PROCESANDO_DECIMAL': {
                '0': 'PROCESANDO_DECIMAL',
                '1': 'PROCESANDO_DECIMAL',
                '2': 'PROCESANDO_DECIMAL',
                '3': 'PROCESANDO_DECIMAL',
                '4': 'PROCESANDO_DECIMAL',
                '5': 'PROCESANDO_DECIMAL',
                '6': 'PROCESANDO_DECIMAL',
                '7': 'PROCESANDO_DECIMAL',
                '8': 'PROCESANDO_DECIMAL',
                '9': 'PROCESANDO_DECIMAL',
                ',': 'ESPERA_COMA_O_FIN_OBJETO',
                '}': 'OBJETO_VALIDO',
                ']': 'ARRAY_VALIDO'
            }
        }

    def procesar_caracter(self, caracter):
        if caracter in [' ', '\n', '\t', '\r']:
            if caracter == '\n':
                self.fila += 1
                self.columna = 1
            else:
                self.columna += 1
            return
        
        if self.estado_actual in self.estados_aceptacion:
            return
        
        if caracter in self.transiciones.get(self.estado_actual, {}):
            self.estado_actual = self.transiciones[self.estado_actual][caracter]
        elif self.estado_actual in {'LEYENDO_LLAVE', 'VALOR_CADENA'}:
            self.estado_actual = self.estado_actual
        else:
            self.reportar_error(f"Error en el carácter '{caracter}' en el estado '{self.estado_actual}'")
        
        self.columna += 1

    def procesar_json(self, texto_json):
        self.fila = 1
        self.columna = 1
        self.errores.clear()
        self.estado_actual = 'INICIO'

        for caracter in texto_json:
            try:
                self.procesar_caracter(caracter)
            except ValueError as e:
                print(e)
                return False
        
        return self.estado_actual in self.estados_aceptacion

    def reportar_errores_csv(self, ruta_csv):
        with open(ruta_csv, mode='w', newline='', encoding='utf-8') as archivo_csv:
            escritor_csv = csv.DictWriter(archivo_csv, fieldnames=['error', 'fila', 'columna'])
            escritor_csv.writeheader()
            escritor_csv.writerows(self.errores)

    def reportar_error(self, mensaje):
        error = f"{mensaje} en la fila {self.fila}, columna {self.columna}"
        self.errores.append({'error': mensaje, 'fila': self.fila, 'columna': self.columna})
        raise ValueError(error)
