-- Migración para bases de datos que ya ejecutaron schema.sql antes de la
-- checklist de documentos por trámite. Ejecuta SOLO esto (no todo schema.sql
-- de nuevo, o reinsertará los clientes de ejemplo).

alter table documentos add column if not exists tipo text;
