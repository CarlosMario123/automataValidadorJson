from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for, send_file
import os
from models.automata_json import AutomataJSON  
from utils.file_utils import allowed_file
import time 

autoMataJson = Blueprint('autoMataJson', __name__, url_prefix="/autoMataJson")


@autoMataJson.route('/')
def upload_form():
    return render_template("upload.html")


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

        with open(file_path, 'r', encoding='utf-8') as f:
            contenido = f.read()

        automata = AutomataJSON() 
        es_json_valido = automata.procesar_json(contenido)

        if not es_json_valido:
            
            nombre_base, _ = os.path.splitext(filename)
            timestamp = int(time.time())  # Para generar un valor unico
            csv_filename = f"{nombre_base}_errores_{timestamp}.csv"
            csv_path = os.path.join(current_app.config['UPLOAD_FOLDER'], csv_filename)

            # Guardar los errores en el archivo CSV
            automata.reportar_errores_csv(csv_path)
            jsonProcesado =automata.json_procesado
            flash(f'El archivo {filename} no contiene un JSON válido. Se ha generado un informe de errores.', 'error')

       
            return redirect(url_for('autoMataJson.upload_form', csv_filename=csv_filename,jsonProcesado=jsonProcesado))

        flash(f'El archivo {filename} contiene un JSON válido', 'success')
        return redirect(url_for('autoMataJson.upload_form'))

    flash('Tipo de archivo no permitido. Solo archivos .txt', 'error')
    return redirect(url_for('autoMataJson.upload_form'))


@autoMataJson.route('/download_report/<filename>')
def download_report(filename):
    csv_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True, download_name=filename, mimetype='text/csv')
    else:
        flash('No se ha generado ningún informe de errores', 'error')
        return redirect(url_for('autoMataJson.upload_form'))

