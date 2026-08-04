-- Esquema para docgestoria en Supabase (Postgres)
-- Ejecutar en Supabase: Project > SQL Editor > New query > pegar y Run

create table if not exists clientes (
  id serial primary key,
  nombre text not null,
  email text,
  tel text,
  dni text,
  tramite text,
  estado text not null default 'pendiente' check (estado in ('pendiente', 'en-curso', 'completado')),
  progreso integer not null default 0 check (progreso between 0 and 100),
  alta text,
  initials text,
  color text default 'blue',
  created_at timestamptz not null default now()
);

create table if not exists documentos (
  id serial primary key,
  nombre text not null,
  cliente_id integer references clientes(id) on delete cascade,
  cliente text,
  tramite text,
  tipo text,
  fecha text,
  estado text not null default 'pendiente' check (estado in ('pendiente', 'aprobado', 'rechazado')),
  size text,
  archivo_path text,
  created_at timestamptz not null default now()
);

-- Por si la tabla ya existía de una instalación previa sin estas columnas.
alter table documentos add column if not exists tipo text;
-- Ruta del archivo real dentro del bucket "Tramites" de Supabase Storage.
alter table documentos add column if not exists archivo_path text;
-- Borrado en cascada: al eliminar un cliente se eliminan sus documentos
-- (por si la tabla ya existía con ON DELETE SET NULL).
alter table documentos drop constraint if exists documentos_cliente_id_fkey;
alter table documentos
  add constraint documentos_cliente_id_fkey
  foreign key (cliente_id) references clientes(id) on delete cascade;

create table if not exists actividad (
  id serial primary key,
  texto text not null,
  tiempo text,
  tipo text default 'blue',
  created_at timestamptz not null default now()
);

-- Datos de ejemplo (los mismos que traía la app), opcional.
insert into clientes (nombre, email, tel, dni, tramite, estado, progreso, alta, initials, color) values
  ('María García', 'maria.garcia@email.com', '+34 612 345 678', '12345678A', 'Constitución S.L.', 'en-curso', 60, '12 jun 2025', 'MG', 'blue'),
  ('Juan López', 'juan.lopez@email.com', '+34 634 567 890', '87654321B', 'Declaración renta', 'pendiente', 25, '8 jun 2025', 'JL', 'amber'),
  ('Ana Sánchez', 'ana.sanchez@email.com', '+34 645 678 901', '11223344C', 'Herencia', 'completado', 100, '3 jun 2025', 'AS', 'green'),
  ('Pedro Martín', 'pedro.martin@email.com', '+34 656 789 012', '44332211D', 'Autónomo alta', 'pendiente', 40, '2 jun 2025', 'PM', 'purple'),
  ('Laura Romero', 'laura.romero@email.com', '+34 667 890 123', '55667788E', 'Compraventa inmueble', 'en-curso', 55, '28 may 2025', 'LR', 'red')
on conflict do nothing;

insert into documentos (nombre, cliente_id, cliente, tramite, tipo, fecha, estado, size) values
  ('DNI_mariagarcía.jpg', 1, 'María García', 'Constitución S.L.', 'DNI/NIE de los socios', 'Hoy 10:24', 'pendiente', '120 KB'),
  ('escritura_contrato.pdf', 5, 'Laura Romero', 'Compraventa inmueble', 'Escritura de compraventa', 'Hoy 09:10', 'pendiente', '2.4 MB'),
  ('modelo_036.pdf', 4, 'Pedro Martín', 'Autónomo alta', 'Modelo 036/037', 'Ayer 17:02', 'pendiente', '340 KB'),
  ('certificado_empadronamiento.pdf', 3, 'Ana Sánchez', 'Herencia', 'Certificado de empadronamiento', 'Lun 11:20', 'aprobado', '180 KB'),
  ('DNI_reverso.jpg', 1, 'María García', 'Constitución S.L.', 'DNI/NIE de los socios', '12 jun 10:30', 'aprobado', '98 KB'),
  ('IRPF_anterior.pdf', 2, 'Juan López', 'Declaración renta', 'Certificado de retenciones (IRPF)', '9 jun 14:00', 'aprobado', '560 KB')
on conflict do nothing;

insert into actividad (texto, tiempo, tipo) values
  ('María García subió 2 documentos nuevos', 'Hace 12 min', 'blue'),
  ('Juan López tiene docs pendientes desde hace 3 días', 'Hace 2 horas', 'amber'),
  ('Trámite de Ana Sánchez marcado como completado', 'Ayer, 11:30', 'green'),
  ('Pedro Martín se registró en la app', 'Lun, 09:15', 'blue'),
  ('Laura Romero aprobó los términos y condiciones', 'Vie, 14:50', 'green')
on conflict do nothing;
