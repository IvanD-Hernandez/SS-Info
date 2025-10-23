DO $$
DECLARE
  v_user text := 'principaleve';
  v_pass text := 'GotoDidNothingWrong';
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = v_user) THEN
    EXECUTE format('CREATE USER %I WITH PASSWORD %L', v_user, v_pass);
  END IF;
END$$;

DO $$
DECLARE
  v_db   text := 'livergton';
  v_user text := 'principaleve';
BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = v_db) THEN
    EXECUTE format('CREATE DATABASE %I OWNER %I', v_db, v_user);
  END IF;
  EXECUTE format('ALTER DATABASE %I OWNER TO %I', v_db, v_user);
END$$;

\connect livergton

ALTER SCHEMA public OWNER TO principaleve;
GRANT ALL PRIVILEGES ON SCHEMA public TO principaleve;
GRANT ALL PRIVILEGES ON DATABASE livergton TO principaleve;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;
