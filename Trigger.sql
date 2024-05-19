CREATE OR REPLACE FUNCTION username_validation()
RETURNS trigger AS
$$
    BEGIN
    IF (NEW.username IN (SELECT usernmae FROM PENGGUNA))
    THEN RAISE EXCEPTION 'Username sudah pernah didaftarkan';
    END IF;
    RETURN NEW;
    END;
$$
LANGUAGE plpgsql;


CREATE TRIGGER username_validation
BEFORE INSERT ON PENGGUNA
FOR EACH ROW
EXECUTE PROCEDURE username_validation();


