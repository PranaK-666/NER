from flask import Flask,redirect,url_for,render_template,request
import pandas as pd
import re
import PyPDF2
from PyPDF2 import PdfReader

# NLP pkgs
import spacy
from spacy import displacy
nlp = spacy.load('en_ner_bc5cdr_md')
from flaskext.markdown import Markdown

# Init App
app = Flask(__name__)
Markdown(app)

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/extract',methods=["GET","POST"])
def ectract():
    if request.method == 'POST':
        f = request.files['file']
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        words = re.sub("[^A-Za-z" "]+", " ", text).lower()
        docx = nlp(words)
        Dataframe=[(ent.text,ent.label_) for ent in docx.ents]
        uniue_char = []
        for c in Dataframe:
            if not c in uniue_char:
                uniue_char.append(c)
        df=pd.DataFrame(uniue_char,columns=['Entity','Disease / Chemical'])
        html = displacy.render(docx,style='ent')
        html = html.replace("\n\n","\n")
        result = HTML_WRAPPER.format(df)

    return render_template("results.html",tables=[df.to_html(classes='data')],titles=['df.columns.values'],result=result)

if __name__=='__main__':
    app.run(debug=True)