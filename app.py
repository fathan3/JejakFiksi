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

def hitung_bm25_params(dataset):
    n_dokumen = len(dataset)
    docs_tokens = [preprocess(d['sinopsis']) for d in dataset]
    
    doc_lengths = [len(doc) for doc in docs_tokens]
    avgdl = sum(doc_lengths) / n_dokumen if n_dokumen > 0 else 1
    
    df_counts = {}
    for doc in docs_tokens:
        for kata in set(doc):
            df_counts[kata] = df_counts.get(kata, 0) + 1
            
    idf_bm25 = {}
    for kata, n_q in df_counts.items():
        idf_bm25[kata] = math.log(((n_dokumen - n_q + 0.5) / (n_q + 0.5)) + 1.0)
        
    return docs_tokens, doc_lengths, avgdl, idf_bm25

def bm25_score(query_tokens, doc_tokens, doc_len, avgdl, idf_bm25, k1=1.5, b=0.75):
    score = 0.0
    for q in query_tokens:
        if q in idf_bm25:
            f_q_D = doc_tokens.count(q)
            if f_q_D > 0:
                numerator = f_q_D * (k1 + 1)
                denominator = f_q_D + k1 * (1 - b + b * (doc_len / avgdl))
                score += idf_bm25[q] * (numerator / denominator)
    return score

with open('dataset_final_search_engine (1).json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)
vocab, idf_map, vektor_dokumen = hitung_tfidf_manual(dataset)
docs_tokens, doc_lengths, avgdl, idf_bm25 = hitung_bm25_params(dataset)


@app.route('/', methods=['GET', 'POST'])
def index():
    query = ""
    method = "cosine"
    hasil_cosine = []
    hasil_bm25 = []
    if request.method == 'POST':
        query = request.form.get('keyword')
        method = request.form.get('method', 'cosine')
        query_tokens = preprocess(query)
        
        if method == 'cosine':
            # Calculate Cosine Similarity
            vektor_query = [query_tokens.count(kata) * idf_map.get(kata, 0) for kata in vocab]
            for i in range(len(vektor_dokumen)):
                skor = cosine_similarity(vektor_query, vektor_dokumen[i])
                if skor > 0:
                    hasil_cosine.append({
                        "judul": dataset[i]['judul'],
                        "sinopsis": dataset[i]['sinopsis'],
                        "skor": round(skor, 4),
                        "url": dataset[i]['url']
                    })
            hasil_cosine = sorted(hasil_cosine, key=lambda x: x['skor'], reverse=True)[:10]
            
        elif method == 'bm25':
            # Calculate BM25
            for i in range(len(dataset)):
                skor = bm25_score(query_tokens, docs_tokens[i], doc_lengths[i], avgdl, idf_bm25)
                if skor > 0:
                    hasil_bm25.append({
                        "judul": dataset[i]['judul'],
                        "sinopsis": dataset[i]['sinopsis'],
                        "skor": round(skor, 4),
                        "url": dataset[i]['url']
                    })
            hasil_bm25 = sorted(hasil_bm25, key=lambda x: x['skor'], reverse=True)[:10]

    return render_template('index.html', query=query, method=method, hasil_cosine=hasil_cosine, hasil_bm25=hasil_bm25)

if __name__ == '__main__':
    app.run(debug=True)