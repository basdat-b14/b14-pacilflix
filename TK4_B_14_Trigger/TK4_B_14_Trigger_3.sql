CREATE OR REPLACE FUNCTION check_ulasan_duplikat()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM "PacilFlix"."ULASAN"
        WHERE id_tayangan = NEW.id_tayangan AND username = NEW.username
    ) THEN
        RAISE EXCEPTION '% sudah pernah membuat ulasan untuk tayangan ini', NEW.username;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_ulasan_duplikat_trigger
BEFORE INSERT ON "PacilFlix"."ULASAN"
FOR EACH ROW
EXECUTE FUNCTION check_ulasan_duplikat();