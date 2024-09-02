DO $$
BEGIN
-- Check if the role exists
IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'postgres') THEN
-- Create the role if it doesn't exist
CREATE ROLE postgres WITH LOGIN PASSWORD 'password';
ELSE
-- Update the role if it exists
ALTER ROLE postgres WITH LOGIN PASSWORD 'password';
END IF;
END $$;

-- Grant all privileges on the database to the role
GRANT ALL PRIVILEGES ON DATABASE crypto_db TO postgres;

-- Grant all privileges on the schema to the role
GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;
