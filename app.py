from flask import Flask, render_template, request, jsonify, redirect, url_for
from data import clientes, documentos, actividad

app = Flask(__name__)

@app.route("/")
def dashboard():
    stats = {
        "clientes_activos": len(clientes),
        "docs_pendientes": sum(1 for d in documentos if d["estado"] == "pendiente"),
        "completados": sum(1 for c in clientes if c["estado"] == "completado"),
        "en_revision": sum(1 for d in documentos if d["estado"] == "pendiente"),
    }
    recientes = list(enumerate(clientes[:5]))
    docs_recientes = [d for d in documentos if d["estado"] == "pendiente"][:3]
    return render_template("dashboard.html", stats=stats, clientes=recientes,
                           docs=docs_recientes, actividad=actividad, active="dashboard")

@app.route("/clientes")
def vista_clientes():
    estado = request.args.get("estado", "todos")
    filtrados = clientes if estado == "todos" else [c for c in clientes if c["estado"] == estado]
    filtrados_idx = [(clientes.index(c), c) for c in filtrados]
    return render_template("clientes.html", clientes=filtrados_idx, estado=estado, active="clientes")

@app.route("/clientes/<int:idx>")
def detalle_cliente(idx):
    if idx < 0 or idx >= len(clientes):
        return redirect(url_for("vista_clientes"))
    cliente = clientes[idx]
    docs_cliente = [d for d in documentos if d["cliente_id"] == idx]
    return render_template("detalle.html", cliente=cliente, docs=docs_cliente,
                           idx=idx, active="clientes")

@app.route("/clientes/nuevo", methods=["POST"])
def nuevo_cliente():
    data = request.get_json()
    nuevo = {
        "nombre": data.get("nombre", "") + " " + data.get("apellidos", ""),
        "email": data.get("email", ""),
        "tel": data.get("tel", ""),
        "dni": data.get("dni", ""),
        "tramite": data.get("tramite", ""),
        "estado": "pendiente",
        "progreso": 0,
        "alta": "Hoy",
        "initials": (data.get("nombre","N")[:1] + data.get("apellidos","C")[:1]).upper(),
        "color": "blue",
    }
    clientes.insert(0, nuevo)
    return jsonify({"ok": True, "nombre": nuevo["nombre"]})

@app.route("/documentos")
def vista_documentos():
    docs_idx = list(enumerate(documentos))
    return render_template("documentos.html", documentos=docs_idx, active="documentos")

@app.route("/documentos/<int:idx>/aprobar", methods=["POST"])
def aprobar_doc(idx):
    if 0 <= idx < len(documentos):
        documentos[idx]["estado"] = "aprobado"
    return jsonify({"ok": True})

@app.route("/documentos/<int:idx>/rechazar", methods=["POST"])
def rechazar_doc(idx):
    if 0 <= idx < len(documentos):
        documentos[idx]["estado"] = "rechazado"
    return jsonify({"ok": True})

@app.route("/expedientes")
def vista_expedientes():
    clientes_idx = list(enumerate(clientes))
    return render_template("expedientes.html", clientes=clientes_idx, active="expedientes")

@app.route("/notificaciones")
def vista_notificaciones():
    return render_template("notificaciones.html", actividad=actividad, active="notificaciones")

@app.route("/ajustes")
def vista_ajustes():
    return render_template("ajustes.html", active="ajustes")

if __name__ == "__main__":
    app.run(debug=True)
