from flask import Flask, request, send_file, jsonify
import os
import signal
from werkzeug.serving import make_server
from threading import Event
from docx import Document
import PyPDF2
import csv

app = Flask(__name__)

UPLOAD_FOLDER = "upload"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
server_ready = Event()


@app.route('/upload',methods=["POST"])
def upload_file():
   

   if "file" not in request.files:
       return jsonify({"error": "No file part in request."}), 400
    
   file = request.files["file"]
   if file.filename == "":
        return jsonify({"error": "No selected file."}), 400
    
   file_path = os.path.join(UPLOAD_FOLDER, file.filename)
   file.save(file_path)
   return jsonify({"message": f"File {file.filename} uploaded successfully."}), 200

@app.route('/download/<filename>',methods=["GET"])
def download_file(filename):

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found."}), 404

@app.route('/list_files', methods=["GET"])
def list_files():
    
    try:
       
        files = os.listdir(UPLOAD_FOLDER)  # Ensure this path is correct
        print(f"Files in directory: {files}")
        return jsonify({"files": files}), 200
    
    except Exception as e:
        print(f"Invalid Token Error: {e}")
        return jsonify({"error": "Invalid token"}), 500
    
@app.route('/view/<filename>', methods =["GET"])
def view_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "file not found."}), 404
    
    try:
        if filename.lower().endswith(".docx"):
            doc = Document(file_path)
            content = "\n".join([para.text for para in doc.paragraphs])

        elif filename.lower().endswith(".pdf"):
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                content=""
                for page in pdf_reader.pages:
                    content += page.extract_text()    
        
        elif filename.lower().endswith(".csv"):
            with open(file_path, "r", encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                content= "\n".join([", ".join(row) for row in csv_reader])

        else:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        return  jsonify({"filename": filename, "content": content}), 200
    except Exception as e:
        return jsonify({"error": f"failed to read file: {str(e)}"}), 500


@app.route('/shutdown', methods=["POST"])
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"message": "Server shutting down..."}), 200


def run_server():
    http_server = make_server('127.0.0.1', 5000, app)
    server_ready.set()
    http_server.serve_forever()

   
if __name__=="__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)