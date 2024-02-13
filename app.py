from flask import Flask, request, render_template, jsonify
import PyPDF2
import io

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        return 'No file part'
    file = request.files['pdf_file']
    if file.filename == '':
        return 'No selected file'
    if file and file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
        word_count = len(text.split())
        # return jsonify({"message": f"The PDF contains {'more' if word_count > 5 else 'less'} than 5 words.", "word_count": word_count})
        word_count = len(text.split())
        message = f"The PDF contains {'more' if word_count > 5 else 'less'} than 5 words."
        return render_template('result.html', message=message, word_count=word_count)
    else:
        return 'Invalid file type'
if __name__ == '__main__':
    app.run(debug=True)
