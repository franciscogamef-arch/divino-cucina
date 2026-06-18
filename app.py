from flask import Flask, render_template, request, jsonify
import json, os, uuid

app = Flask(__name__)
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DADOS_FILE = os.path.join(BASE_DIR, "dados.json")
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED    = {"png","jpg","jpeg","gif","webp"}
os.makedirs(UPLOAD_DIR, exist_ok=True)

def allowed(f): return "." in f and f.rsplit(".",1)[1].lower() in ALLOWED
def carregar():
    if not os.path.exists(DADOS_FILE): return []
    return json.load(open(DADOS_FILE, encoding="utf-8"))
def salvar(p): json.dump(p, open(DADOS_FILE,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

@app.route("/")
def index(): return render_template("index.html")

@app.route("/api/pratos", methods=["GET"])
def listar(): return __import__("flask").jsonify(carregar())

@app.route("/api/pratos", methods=["POST"])
def criar():
    p = carregar()
    d = request.get_json()
    novo = {"id":str(uuid.uuid4()),"nome":d.get("nome",""),"descricao":d.get("descricao",""),"preco":float(d.get("preco",0)),"imagem_url":d.get("imagem_url",""),"passos":d.get("passos",[])}
    p.insert(0, novo); salvar(p)
    return __import__("flask").jsonify(novo), 201

@app.route("/api/pratos/<id>", methods=["PUT"])
def atualizar(id):
    p = carregar(); d = request.get_json()
    for x in p:
        if x["id"]==id:
            x.update({"nome":d.get("nome",x["nome"]),"descricao":d.get("descricao",x["descricao"]),"preco":float(d.get("preco",x["preco"])),"imagem_url":d.get("imagem_url",x["imagem_url"]),"passos":d.get("passos",x["passos"])})
            salvar(p); return __import__("flask").jsonify(x)
    return __import__("flask").jsonify({"erro":"nao encontrado"}), 404

@app.route("/api/pratos/<id>", methods=["DELETE"])
def deletar(id):
    p = carregar(); nova=[x for x in p if x["id"]!=id]
    if len(nova)==len(p): return __import__("flask").jsonify({"erro":"nao encontrado"}), 404
    salvar(nova); return __import__("flask").jsonify({"ok":True})

@app.route("/api/upload", methods=["POST"])
def upload():
    if "foto" not in request.files: return __import__("flask").jsonify({"erro":"sem arquivo"}), 400
    foto=request.files["foto"]
    if not allowed(foto.filename): return __import__("flask").jsonify({"erro":"invalido"}), 400
    ext=foto.filename.rsplit(".",1)[1].lower(); nome=uuid.uuid4().hex+"."+ext
    foto.save(os.path.join(UPLOAD_DIR,nome))
    return __import__("flask").jsonify({"url":"/static/uploads/"+nome})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)), debug=False)
