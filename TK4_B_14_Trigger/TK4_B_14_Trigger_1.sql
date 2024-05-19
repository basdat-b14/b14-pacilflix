-- Function & Trigger untuk validasi apakah username sudah ada atau belum

CREATE OR REPLACE FUNCTION check_username_exists()
RETURNS TRIGGER AS $$
 BEGIN
     IF EXISTS (SELECT 1 FROM pengguna WHERE username = NEW.username) THEN
         RAISE EXCEPTION 'Username "%" sudah terdaftar', NEW.username;
     END IF;
     RETURN NEW;
 END;
 $$ LANGUAGE plpgsql;



CREATE TRIGGER trigger_check_username_exists
BEFORE INSERT ON "PacilFlix"."PENGGUNA"
FOR EACH ROW
EXECUTE FUNCTION check_username_exists();


CREATE OR REPLACE PROCEDURE check_username_exists(
    IN p_username VARCHAR(255),
    OUT p_exists BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM "PENGGUNA" WHERE username = p_username) THEN
        p_exists := TRUE;
    ELSE
        p_exists := FALSE;
    END IF;
END;
$$;
