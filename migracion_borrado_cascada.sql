-- Migración: al borrar un cliente, borrar también sus documentos (cascada).
-- Antes el FK era ON DELETE SET NULL (dejaba los documentos huérfanos).
-- Ejecuta SOLO esto en el SQL Editor de Supabase.

alter table documentos drop constraint if exists documentos_cliente_id_fkey;

alter table documentos
  add constraint documentos_cliente_id_fkey
  foreign key (cliente_id) references clientes(id) on delete cascade;
