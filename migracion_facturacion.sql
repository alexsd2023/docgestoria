-- Migración: tablas de Facturación.
-- Ejecuta esto en el SQL Editor de Supabase.

create table if not exists facturas (
  id serial primary key,
  numero text,
  cliente_id integer references clientes(id) on delete set null,
  cliente text,
  fecha text,
  base_imponible numeric(10,2) not null default 0,
  iva_porcentaje integer not null default 21 check (iva_porcentaje in (10, 21)),
  iva_importe numeric(10,2) not null default 0,
  total numeric(10,2) not null default 0,
  created_at timestamptz not null default now()
);

create table if not exists factura_lineas (
  id serial primary key,
  factura_id integer references facturas(id) on delete cascade,
  concepto text not null,
  importe numeric(10,2) not null default 0
);
