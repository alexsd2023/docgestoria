-- Migración para poder adjuntar el archivo real de cada documento
-- (subido al bucket "Tramites" de Supabase Storage).
-- Ejecuta SOLO esto en el SQL Editor de Supabase (no todo schema.sql de nuevo).

alter table documentos add column if not exists archivo_path text;
