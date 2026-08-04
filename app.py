from flask import Flask, render_template, request, jsonify, redirect, url_for
import data
import catalogo
import storage

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
    requeridos = catalogo.documentos_requeridos(cliente["tramite"])

    checklist = []
    tipos_requeridos = set(requeridos)
    for tipo in requeridos:
        doc = next((d for d in docs_cliente if d.get("tipo") == tipo), None)
        checklist.append({"tipo": tipo, "doc": doc})

    otros_docs = [d for d in docs_cliente if d.get("tipo") not in tipos_requeridos]

    return render_template(
        "detalle.html",
        cliente=cliente,
        docs=docs_cliente,
        checklist=checklist,
        otros_docs=otros_docs,
        idx=idx,
        active="clientes",
    )


@app.route("/clientes/<int:idx>/documentos/solicitar", methods=["POST"])
def solicitar_documento(idx):
    cliente = data.obtener_cliente(idx)
    if not cliente:
        return jsonify({"ok": False, "error": "cliente no encontrado"}), 404
    body = request.get_json() or {}
    tipo = body.get("tipo", "")
    nuevo = data.crear_documento(
        nombre=tipo,
        cliente_id=idx,
        cliente=cliente["nombre"],
        tramite=cliente["tramite"],
        tipo=tipo,
        fecha="Hoy",
        size="-",
    )
    return jsonify({"ok": True, "documento": nuevo})


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
    return render_template(
        "documentos.html",
        documentos=documentos,
        grupos_tramites=catalogo.GRUPOS_TRAMITES,
        clientes_documentos=data.clientes_de_documentos(),
        active="documentos",
    )


@app.route("/documentos/<int:idx>/aprobar", methods=["POST"])
def aprobar_doc(idx):
    data.actualizar_estado_documento(idx, "aprobado")
    return jsonify({"ok": True})


@app.route("/documentos/<int:idx>/rechazar", methods=["POST"])
def rechazar_doc(idx):
    data.actualizar_estado_documento(idx, "rechazado")
    return jsonify({"ok": True})


@app.route("/documentos/<int:idx>/archivo", methods=["POST"])
def subir_archivo_documento(idx):
    documento = data.obtener_documento(idx)
    if not documento:
        return jsonify({"ok": False, "error": "Documento no encontrado"}), 404

    archivo = request.files.get("archivo")
    if not archivo or not archivo.filename:
        return jsonify({"ok": False, "error": "No se ha seleccionado ningún archivo"}), 400

    cliente_id = documento.get("cliente_id") or "sin-cliente"
    path = f"{cliente_id}/{idx}_{archivo.filename}"
    ok, error = storage.subir_archivo(path, archivo.read(), archivo.filename)
    if not ok:
        return jsonify({"ok": False, "error": error}), 500

    data.actualizar_archivo_documento(idx, path)
    return jsonify({"ok": True, "archivo_path": path})


@app.route("/documentos/<int:idx>/descargar")
def descargar_documento(idx):
    documento = data.obtener_documento(idx)
    if not documento or not documento.get("archivo_path"):
        return "Este documento no tiene ningún archivo adjunto todavía.", 404

    url, error = storage.url_firmada(
        documento["archivo_path"],
        forzar_descarga=True,
        nombre_descarga=documento["nombre"],
    )
    if error:
        return f"No se pudo generar el enlace de descarga: {error}", 500
    return redirect(url)


@app.route("/documentos/<int:idx>/url-previa")
def url_previa_documento(idx):
    documento = data.obtener_documento(idx)
    if not documento:
        return jsonify({"ok": False, "error": "Documento no encontrado"}), 404
    if not documento.get("archivo_path"):
        return jsonify({"ok": True, "url": None})

    url, error = storage.url_firmada(documento["archivo_path"])
    if error:
        return jsonify({"ok": False, "error": error}), 500
    return jsonify({"ok": True, "url": url, "nombre": documento["nombre"]})


@app.route("/expedientes")
def vista_expedientes():
    clientes = data.listar_clientes()
    return render_template(
        "expedientes.html",
        clientes=clientes,
        grupos_tramites=catalogo.GRUPOS_TRAMITES,
        active="expedientes",
    )


@app.route("/buscar")
def vista_buscar():
    q = request.args.get("q", "").strip()
    resultados = data.buscar_clientes(q) if q else []
    return render_template("buscar.html", query=q, clientes=resultados, active="buscar")


@app.route("/api/buscar")
def api_buscar():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"resultados": []})
    resultados = data.buscar_clientes(q, limit=8)
    return jsonify({"resultados": resultados})


@app.route("/estadisticas")
def vista_estadisticas():
    total_clientes = data.contar_clientes()
    total_documentos = data.contar_documentos()
    clientes_estado = data.estadisticas_clientes_por_estado()
    docs_estado = data.estadisticas_documentos_por_estado()
    por_tramite = data.clientes_por_tramite()
    progreso = data.progreso_medio()

    tasa_aprobacion = (
        round(docs_estado["aprobado"] / total_documentos * 100) if total_documentos else 0
    )

    por_categoria = {}
    for fila in por_tramite:
        cat = catalogo.categoria_de_tramite(fila["tramite"])
        por_categoria[cat] = por_categoria.get(cat, 0) + fila["n"]
    por_categoria = sorted(por_categoria.items(), key=lambda item: -item[1])

    return render_template(
        "estadisticas.html",
        total_clientes=total_clientes,
        total_documentos=total_documentos,
        clientes_estado=clientes_estado,
        docs_estado=docs_estado,
        por_tramite=por_tramite[:10],
        por_categoria=por_categoria,
        progreso_medio=progreso,
        tasa_aprobacion=tasa_aprobacion,
        active="estadisticas",
    )


@app.route("/notificaciones")
def vista_notificaciones():
    actividad = data.listar_actividad()
    return render_template("notificaciones.html", actividad=actividad, active="notificaciones")


@app.route("/ajustes")
def vista_ajustes():
    return render_template("ajustes.html", active="ajustes")


@app.route("/facturacion")
def vista_facturacion():
    return render_template("facturacion.html", facturas=[], active="facturacion")


if __name__ == "__main__":
    app.run(debug=True)
