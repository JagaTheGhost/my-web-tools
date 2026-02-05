# MyWebTools - Web-Based File Processing Suite

A modern, secure web application for converting, compressing, and manipulating images, PDFs, and documents. Built with Flask and deployed on Heroku.

## Features

### 🖼️ Image Converter (Prisma Convert)
- Convert images between **JPG**, **PNG**, and **WEBP** formats
- Drag-and-drop interface with live preview
- Client-side processing for maximum security
- Automatic quality optimization

### 📉 File Compressor (OmniCompress)
- **Image compression** - Reduce JPG/PNG file sizes
- **PDF compression** - Minimize PDF documents
- **DOCX compression** - Compress Word documents with smart image optimization
- Instant processing with secure handling

### 🔄 Document Converter (DocuPrisma)
- **PDF to Word** (.docx) conversion
- **Word to PDF** conversion
- **PowerPoint to PDF** conversion
- Server-side processing with reliable output

### 📑 PDF Merger
- Combine multiple PDF files into a single document
- Simple multi-select interface
- Preserves document quality

## Tech Stack

- **Backend**: Python Flask
- **Image Processing**: Pillow (PIL)
- **PDF Handling**: pypdf, pdf2docx
- **Document Conversion**: docx2pdf, python-pptx, comtypes
- **Deployment**: Gunicorn + Heroku
- **Frontend**: Responsive HTML5 with modern CSS3

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd MyWebTools
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open in browser:
```
http://localhost:5000
```

## Project Structure

```
MyWebTools/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment config
├── templates/            # HTML templates
│   ├── home.html         # Portal landing page
│   ├── image.html        # Image converter tool
│   ├── compress.html     # File compressor tool
│   ├── convert.html      # Document converter tool
│   └── merge.html        # PDF merger tool
├── uploads/              # Temporary upload folder
└── downloads/            # Processed file output folder
```

## Key Functions

- `compress_image_logic()` - JPEG compression with quality optimization
- `compress_pdf_logic()` - PDF stream compression
- `compress_docx_logic()` - DOCX compression with embedded image optimization
- `merge_pdfs_logic()` - Multi-PDF merging
- `/api/convert` - Multi-format document conversion endpoint

## Dependencies

See [requirements.txt](requirements.txt) for full list:
- Flask
- Pillow
- pypdf
- pdf2docx
- docx2pdf
- gunicorn

## Deployment

Deploy to Heroku using:
```bash
heroku create <app-name>
git push heroku main
```

## Notes

- All file uploads are temporary and auto-cleaned
- Image converter uses client-side processing for privacy
- Document conversions use server-side processing via system libraries
- Maximum file sizes depend on server configuration

## License

Open source project.
