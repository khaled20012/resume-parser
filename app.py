from flask import Flask, request, render_template
import spacy
from docx import Document

app = Flask(__name__)
nlp = spacy.load("assets\model_cv\model-best")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/parse", methods=["POST"])
def parse_resume():
    if "resume" not in request.files:
        return "No file part"
    
    resume_file = request.files["resume"]
    if resume_file.filename == "":
        return "No selected file"
    
    # Check file extension to determine the format
    if resume_file.filename.endswith(".pdf"):
        text = parse_pdf(resume_file)
    elif resume_file.filename.endswith(".docx"):
        text = parse_docx(resume_file)
    else:
        return "Unsupported file format"
    
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    return render_template("result.html", entities=entities)

def parse_pdf(file):
    # Placeholder implementation
    return ""

def parse_docx(file):
    docx_file = Document(file)
    text = ""
    for paragraph in docx_file.paragraphs:
        text += paragraph.text + "\n"
    return text

if __name__ == "__main__":
    app.run(debug=True)
