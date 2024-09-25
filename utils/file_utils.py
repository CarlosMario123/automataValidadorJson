

def allowed_file(filename, allowed_extensions):
    """
    Verifica si el archivo tiene una extensión permitida.
    :param filename: Nombre del archivo
    :param allowed_extensions: Conjunto de extensiones permitidas
    :return: True si la extensión es permitida, False de lo contrario
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
