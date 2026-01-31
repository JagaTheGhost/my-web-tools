import os
import zipfile
import pythoncom
import comtypes.client
from io import BytesIO
from flask import Flask, render_template, request, send_file
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pdf2docx import Converter
from docx2pdf import convert
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- CONFIGURATION ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(basedir, 'downloads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# --- HELPER FUNCTIONS ---
def compress_image_logic(file_stream):
    img = Image.open(file_stream)
    if img.mode in ("RGBA", "P"): img = img.convert("RGB")
    output = BytesIO()
    img.save(output, format="JPEG", quality=60, optimize=True)
    output.seek(0)
    return output, "compressed.jpg"

def compress_pdf_logic(file_stream):
    reader = PdfReader(file_stream)
    writer = PdfWriter()
    for page in reader.pages:
        new_page = writer.add_page(page)
        new_page.compress_content_streams()
    output = BytesIO()
    writer.write(output)
    output.seek(0)
    return output, "compressed.pdf"

def compress_docx_logic(file_stream):
    output = BytesIO()
    with zipfile.ZipFile(file_stream, 'r') as zin:
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename.startswith('word/media/') and item.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        img = Image.open(BytesIO(data))
                        img_buffer = BytesIO()
                        img.convert('RGB').save(img_buffer, 'JPEG', quality=50)
                        data = img_buffer.getvalue()
                    except: pass
                zout.writestr(item, data)
    output.seek(0)
    return output, "compressed.docx"

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/image-tool')
def image_tool():
    return render_template('image.html')

# --- COMPRESSOR TOOL ROUTES ---
@app.route('/compress-tool', methods=['GET', 'POST'])
def compress_tool():
    if request.method == 'POST':
        file = request.files.get('file')
        file_type = request.form.get('type')
        
        if not file: return "No file", 400

        try:
            if file_type == 'image':
                out, name = compress_image_logic(file.stream)
            elif file_type == 'pdf':
                out, name = compress_pdf_logic(file.stream)
            elif file_type == 'doc':
                out, name = compress_docx_logic(file.stream)
            else:
                return "Invalid Type", 400
            
            return send_file(out, as_attachment=True, download_name=name)
        except Exception as e:
            return f"Error: {e}", 500

    return render_template('compress.html')

# --- CONVERTER TOOL ROUTES ---
@app.route('/convert-tool')
def convert_tool():
    return render_template('convert.html')

@app.route('/api/convert', methods=['POST'])
def api_convert():
    try:
        file = request.files['file']
        conversion_type = request.form['type']
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        name_no_ext = os.path.splitext(filename)[0]

        if conversion_type == 'pdf2word':
            out_name = f"{name_no_ext}.docx"
            out_path = os.path.join(app.config['OUTPUT_FOLDER'], out_name)
            cv = Converter(input_path)
            cv.convert(out_path, start=0, end=None)
            cv.close()

        elif conversion_type == 'word2pdf':
            out_name = f"{name_no_ext}.pdf"
            out_path = os.path.join(app.config['OUTPUT_FOLDER'], out_name)
            pythoncom.CoInitialize()
            convert(input_path, out_path)

        elif conversion_type == 'ppt2pdf':
            out_name = f"{name_no_ext}.pdf"
            out_path = os.path.join(app.config['OUTPUT_FOLDER'], out_name)
            pythoncom.CoInitialize()
            ppt = comtypes.client.CreateObject("Powerpoint.Application")
            ppt.Visible = 1 
            deck = ppt.Presentations.Open(input_path)
            deck.SaveAs(out_path, 32)
            deck.Close()
            ppt.Quit()
        
        return send_file(out_path, as_attachment=True, download_name=out_name)
    
    except Exception as e:
        print(e)
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)