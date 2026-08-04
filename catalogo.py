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
        "Pasaporte en vigor (completo, todas las páginas)",
        "Formulario EX-15 cumplimentado",
        "Justificante de pago de la tasa (modelo 790 012)",
        "Justificante del motivo de la solicitud (contrato, oferta de trabajo, compraventa, etc.)",
        "2 fotografías tamaño carnet",
    ],
    "Certificado de Registro de la UE": [
        "Pasaporte o documento de identidad en vigor",
        "Formulario EX-18 cumplimentado",
        "Justificante de pago de la tasa (modelo 790 012)",
        "Documento acreditativo de la actividad (contrato de trabajo, alta de autónomo o matrícula de estudios)",
        "Seguro médico público o privado con cobertura en España",
        "Justificante de medios económicos suficientes",
        "Certificado de empadronamiento",
    ],
    "Tarjeta de Familiar de Ciudadano de la UE": [
        "Pasaporte en vigor",
        "Formulario EX-19 cumplimentado",
        "Certificado de empadronamiento",
        "Justificante de vínculo familiar (libro de familia, certificado de matrimonio o pareja de hecho)",
        "Justificante de pago de la tasa (modelo 790 052)",
        "Certificado de registro o tarjeta del ciudadano de la UE reagrupante",
        "Seguro médico público o privado (si aplica)",
        "3 fotografías tamaño carnet",
    ],
    "Empadronamiento": [
        "DNI/NIE o pasaporte en vigor",
        "Justificante de domicilio (contrato de alquiler o escritura de propiedad)",
        "Último recibo de suministro (agua, luz o gas) a nombre del titular",
        "Autorización del titular de la vivienda y copia de su DNI (si no eres el titular)",
        "Formulario de solicitud de empadronamiento",
    ],
}


def documentos_requeridos(tramite):
    return TRAMITES_DOCUMENTOS.get(tramite, [])
