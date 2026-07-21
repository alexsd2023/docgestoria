from flask import Flask, render_template, request, jsonify, redirect, url_for
import data

app = Flask(__name__)


@app.route("/")
def dashboard():
    stats = {
        "clientes_activos": data.contar_clientes(),
        "docs_pendientes": data.contar_documentos_pendientes(),
        "completados": data.contar_clientes_por_estado("completado"),
        "en_revision": data.contar_documentos_pendientes(),
    }
    recientes = data.clientes_recientes(5)
    docs_recientes = data.documentos_pendientes(3)
    actividad = data.listar_actividad()
    return render_template(
        "dashboard.html",
        stats=stats,
        clientes=recientes,
        docs=docs_recientes,
        actividad=actividad,
        active="dashboard",
    )


@app.route("/clientes")
def vista_clientes():
    estado = request.args.get("estado", "todos")
    clientes = data.listar_clientes(estado)
    return render_template("clientes.html", clientes=clientes, estado=estado, active="clientes")


@app.route("/clientes/<int:idx>")
def detalle_cliente(idx):
    cliente = data.obtener_cliente(idx)
    if not cliente:
        return redirect(url_for("vista_clientes"))
    docs_cliente = data.listar_documentos_por_cliente(idx)
    return render_template(
        "detalle.html", cliente=cliente, docs=docs_cliente, idx=idx, active="clientes"
    )


@app.route("/clientes/nuevo", methods=["POST"])
def nuevo_cliente():
    body = request.get_json()
    nombre_completo = (body.get("nombre", "") + " " + body.get("apellidos", "")).strip()
    initials = (body.get("nombre", "N")[:1] + body.get("apellidos", "C")[:1]).upper()
    nuevo = data.crear_cliente(
        nombre=nombre_completo,
        email=body.get("email", ""),
        tel=body.get("tel", ""),
        dni=body.get("dni", ""),
        tramite=body.get("tramite", ""),
        initials=initials,
        color="blue",
    )
    return jsonify({"ok": True, "nombre": nuevo["nombre"]})


@app.route("/documentos")
def vista_documentos():
    documentos = data.listar_documentos()
    return render_template("documentos.html", documentos=documentos, active="documentos")


@app.route("/documentos/<int:idx>/aprobar", methods=["POST"])
def aprobar_doc(idx):
    data.actualizar_estado_documento(idx, "aprobado")
    return jsonify({"ok": True})


@app.route("/documentos/<int:idx>/rechazar", methods=["POST"])
def rechazar_doc(idx):
    data.actualizar_estado_documento(idx, "rechazado")
    return jsonify({"ok": True})


@app.route("/expedientes")
def vista_expedientes():
    clientes = data.listar_clientes()
    return render_template("expedientes.html", clientes=clientes, active="expedientes")


@app.route("/notificaciones")
def vista_notificaciones():
    actividad = data.listar_actividad()
    return render_template("notificaciones.html", actividad=actividad, active="notificaciones")


@app.route("/ajustes")
def vista_ajustes():
    return render_template("ajustes.html", active="ajustes")


if __name__ == "__main__":
    app.run(debug=True)
