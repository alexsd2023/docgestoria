"""
Catálogo de documentos requeridos por cada tipo de trámite.

Esto define la "checklist" que se muestra en la ficha de cada cliente
(Documentos del expediente). Si un trámite no está en este diccionario
(por ejemplo "Otro"), se muestra la lista simple de documentos subidos
sin checklist.
"""

TRAMITES_DOCUMENTOS = {
    "Constitución S.L.": [
        "DNI/NIE de los socios",
        "Estatutos sociales",
        "Certificado de denominación social",
        "Justificante de capital social",
    ],
    "Declaración renta": [
        "DNI/NIE",
        "Certificado de retenciones (IRPF)",
        "Justificantes de ingresos",
        "Justificantes de gastos deducibles",
    ],
    "Autónomo alta": [
        "DNI/NIE",
        "Modelo 036/037",
        "Justificante de domicilio",
        "Certificado bancario",
    ],
    "Herencia": [
        "DNI/NIE del heredero",
        "Certificado de defunción",
        "Certificado de últimas voluntades",
        "Testamento o declaración de herederos",
        "Certificado de empadronamiento",
        "Escritura de aceptación de herencia",
    ],
    "Compraventa inmueble": [
        "DNI/NIE de las partes",
        "Nota simple registral",
        "Contrato de arras",
        "Escritura de compraventa",
        "Justificante de pago de impuestos",
    ],
    "Obtención de NIE": [
        "Pasaporte",
        "Formulario EX-15",
        "Justificante de pago (tasa 790 012)",
        "Justificante del motivo de solicitud",
    ],
    "Tarjeta de Familiar de Ciudadano de la UE": [
        "Pasaporte",
        "Formulario EX-19",
        "Certificado de empadronamiento",
        "Justificante de vínculo familiar",
        "Justificante de pago (tasa 790 052)",
        "Certificado de inscripción del ciudadano UE",
    ],
    "Empadronamiento": [
        "DNI/NIE o pasaporte",
        "Justificante de domicilio",
        "Formulario de solicitud de empadronamiento",
    ],
}


def documentos_requeridos(tramite):
    return TRAMITES_DOCUMENTOS.get(tramite, [])
