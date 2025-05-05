import fitz  # PyMuPDF
import docx

def extrair_texto_pdf(caminho):
    texto = ""
    with fitz.open(caminho) as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto

def extrair_texto_docx(caminho):
    doc = docx.Document(caminho)
    return "\n".join([p.text for p in doc.paragraphs])

def extrair_texto_arquivo(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        return extrair_texto_pdf("temp.pdf")

    elif uploaded_file.name.endswith(".docx"):
        with open("temp.docx", "wb") as f:
            f.write(uploaded_file.getbuffer())
        return extrair_texto_docx("temp.docx")

    elif uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    else:
        return "Formato não suportado."
