-- create user if not exists

DO
-- change the delimiter
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'sg_test_user') THEN

      RAISE NOTICE 'Role "sg_test_user" already exists. Skipping.';
   ELSE
      CREATE ROLE sg_test_user LOGIN PASSWORD 'sg_test_pwd';
   END IF;
END
-- change back the delimiter
$do$;

-- Create database if it does not exist
-- DO $$ BEGIN
--     IF NOT EXISTS (SELECT FROM pg_catalog.pg_database WHERE datname = 'sg_test_db') THEN
--         -- Create the database
--         CREATE DATABASE sg_test_db;
--     END IF;
-- END $$;
SELECT 'CREATE DATABASE sg_test_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'sg_test_db')\gexec

-- Grant privileges to a user on the database
GRANT ALL PRIVILEGES ON DATABASE sg_test_db TO sg_test_user;