from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, send_file,session
import os
import zipfile
from io import BytesIO
from models.automata_json import AutomataJSON  
from utils.file_utils import allowed_file
from utils.jsonEstruct import arrayToJsonFormated
import time

autoMataJson = Blueprint('autoMataJson', __name__, url_prefix="/autoMataJson")


@autoMataJson.route('/')
def upload_form():
    # Verificar si se ha generado un archivo ZIP para descarga
    filename = request.args.get('filename', None)
    
    jsons = session.get('jsons', [])
    session.pop('jsons', None) 
    return render_template("upload.html", filename=filename,jsons=jsons)


@autoMataJson.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No hay archivo en la solicitud', 'error')
        return redirect(url_for('autoMataJson.upload_form'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No se seleccionó ningún archivo', 'error')
        return redirect(url_for('autoMataJson.upload_form'))
    
    if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        filename = file.filename
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Intentar procesar el archivo
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                contenido = f.read()

            automata = AutomataJSON() 
            json_validos = automata.procesar_json(contenido)  # Obtener JSON válidos

            # Si no se encontraron JSON válidos
            if not json_validos:
                json_validos = []
                flash(f"El archivo {filename} no contiene ninguna cadena JSON válida.", 'error')
                return redirect(url_for('autoMataJson.upload_form'))

            # Si se encontraron JSON válidos
            flash(f"El archivo {filename} contiene {len(json_validos)} cadenas JSON válidas.", 'success')

            # Generar un archivo ZIP con los JSON válidos
            nombre_base, _ = os.path.splitext(filename)
            timestamp = int(time.time())  # Generar un timestamp único
            output_filename = f"{nombre_base}_json_validos_{timestamp}.zip"
            output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], output_filename)

            # Crear el archivo ZIP y agregar cada JSON como un archivo separado
            with zipfile.ZipFile(output_path, 'w') as zipf:
                for i, json_valido in enumerate(json_validos, start=1):
                    json_filename = f"{nombre_base}_json_{i}.json"
                    # Escribir cada JSON en un archivo separado dentro del ZIP
                    zipf.writestr(json_filename, json_valido)

            # Redirigir al formulario de subida con el nombre del archivo ZIP para mostrar el botón de descarga
            
            session['jsons'] = arrayToJsonFormated(json_validos)
            return redirect(url_for('autoMataJson.upload_form',filename=output_filename))

        except Exception as e:
            flash(f"Error procesando el archivo: {str(e)}", 'error')
            return redirect(url_for('autoMataJson.upload_form'))

    else:
        flash('Tipo de archivo no permitido. Solo se permiten archivos .txt.', 'error')
        return redirect(url_for('autoMataJson.upload_form'))


@autoMataJson.route('/download_report/<filename>')
def download_report(filename):
    output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True, download_name=filename, mimetype='application/zip')
    else:
        flash('No se ha generado ningún archivo para descargar.', 'error')
        return redirect(url_for('autoMataJson.upload_form'))
