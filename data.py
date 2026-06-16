clientes = [
    {"nombre": "María García", "email": "maria.garcia@email.com", "tel": "+34 612 345 678",
     "dni": "12345678A", "tramite": "Constitución S.L.", "estado": "en-curso",
     "progreso": 60, "alta": "12 jun 2025", "initials": "MG", "color": "blue"},
    {"nombre": "Juan López", "email": "juan.lopez@email.com", "tel": "+34 634 567 890",
     "dni": "87654321B", "tramite": "Declaración renta", "estado": "pendiente",
     "progreso": 25, "alta": "8 jun 2025", "initials": "JL", "color": "amber"},
    {"nombre": "Ana Sánchez", "email": "ana.sanchez@email.com", "tel": "+34 645 678 901",
     "dni": "11223344C", "tramite": "Herencia", "estado": "completado",
     "progreso": 100, "alta": "3 jun 2025", "initials": "AS", "color": "green"},
    {"nombre": "Pedro Martín", "email": "pedro.martin@email.com", "tel": "+34 656 789 012",
     "dni": "44332211D", "tramite": "Autónomo alta", "estado": "pendiente",
     "progreso": 40, "alta": "2 jun 2025", "initials": "PM", "color": "purple"},
    {"nombre": "Laura Romero", "email": "laura.romero@email.com", "tel": "+34 667 890 123",
     "dni": "55667788E", "tramite": "Compraventa inmueble", "estado": "en-curso",
     "progreso": 55, "alta": "28 may 2025", "initials": "LR", "color": "red"},
]

documentos = [
    {"nombre": "DNI_mariagarcía.jpg", "cliente": "María García", "cliente_id": 0,
     "tramite": "Constitución S.L.", "fecha": "Hoy 10:24", "estado": "pendiente", "size": "120 KB"},
    {"nombre": "escritura_contrato.pdf", "cliente": "Laura Romero", "cliente_id": 4,
     "tramite": "Compraventa inmueble", "fecha": "Hoy 09:10", "estado": "pendiente", "size": "2.4 MB"},
    {"nombre": "modelo_036.pdf", "cliente": "Pedro Martín", "cliente_id": 3,
     "tramite": "Autónomo alta", "fecha": "Ayer 17:02", "estado": "pendiente", "size": "340 KB"},
    {"nombre": "certificado_empadronamiento.pdf", "cliente": "Ana Sánchez", "cliente_id": 2,
     "tramite": "Herencia", "fecha": "Lun 11:20", "estado": "aprobado", "size": "180 KB"},
    {"nombre": "DNI_reverso.jpg", "cliente": "María García", "cliente_id": 0,
     "tramite": "Constitución S.L.", "fecha": "12 jun 10:30", "estado": "aprobado", "size": "98 KB"},
    {"nombre": "IRPF_anterior.pdf", "cliente": "Juan López", "cliente_id": 1,
     "tramite": "Declaración renta", "fecha": "9 jun 14:00", "estado": "aprobado", "size": "560 KB"},
]

actividad = [
    {"texto": "María García subió 2 documentos nuevos", "tiempo": "Hace 12 min", "tipo": "blue"},
    {"texto": "Juan López tiene docs pendientes desde hace 3 días", "tiempo": "Hace 2 horas", "tipo": "amber"},
    {"texto": "Trámite de Ana Sánchez marcado como completado", "tiempo": "Ayer, 11:30", "tipo": "green"},
    {"texto": "Pedro Martín se registró en la app", "tiempo": "Lun, 09:15", "tipo": "blue"},
    {"texto": "Laura Romero aprobó los términos y condiciones", "tiempo": "Vie, 14:50", "tipo": "green"},
]
