CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';

GRANT SELECT ON ALL TABLES IN SCHEMA public TO replicator;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO replicator;

SELECT pg_create_physical_replication_slot('replication_slot');
