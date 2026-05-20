from flask import Flask, render_template, request
import math
import re
import json

app = Flask(__name__)

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.split()

def hitung_tfidf_manual(dataset):
    n_dokumen = len(dataset)
    docs_tokens = [preprocess(d['sinopsis']) for d in dataset]
    vocab = []
    for doc in docs_tokens:
        for kata in doc:
            if kata not in vocab: vocab.append(kata)
    
    df_counts = {kata: sum(1 for doc in docs_tokens if kata in doc) for kata in vocab}
    idf_map = {kata: math.log10(n_dokumen / df_counts[kata]) for kata in vocab}
    
    vektor_dokumen = []
    for doc in docs_tokens:
        vektor = [doc.count(kata) * idf_map[kata] for kata in vocab]
        vektor_dokumen.append(vektor)
        
    return vocab, idf_map, vektor_dokumen

def cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a**2 for a in vec_a)
    norm_b = sum(b**2 for b in vec_b)
    if norm_a == 0 or norm_b == 0: return 0
    return dot_product / (math.sqrt(norm_a) * math.sqrt(norm_b))

with open('dataset_final_search_engine (1).json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)
vocab, idf_map, vektor_dokumen = hitung_tfidf_manual(dataset)


@app.route('/', methods=['GET', 'POST'])
def index():
    query = ""
    hasil = []
    if request.method == 'POST':
        query = request.form.get('keyword')
        query_tokens = preprocess(query)
        vektor_query = [query_tokens.count(kata) * idf_map.get(kata, 0) for kata in vocab]
        
        for i in range(len(vektor_dokumen)):
            skor = cosine_similarity(vektor_query, vektor_dokumen[i])
            if skor > 0:
                hasil.append({
                    "judul": dataset[i]['judul'],
                    "sinopsis": dataset[i]['sinopsis'],
                    "skor": round(skor, 4),
                    "url": dataset[i]['url']
                })
        hasil = sorted(hasil, key=lambda x: x['skor'], reverse=True)

    return render_template('index.html', query=query, hasil=hasil)

if __name__ == '__main__':
    app.run(debug=True)