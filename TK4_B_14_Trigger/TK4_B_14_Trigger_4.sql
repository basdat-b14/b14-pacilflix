CREATE OR REPLACE FUNCTION check_download_duration()
RETURNS TRIGGER AS $$
BEGIN
  -- Mengecek apakah tayangan telah terunduh lebih dari 1 hari
  IF (CURRENT_TIMESTAMP - OLD."timestamp" > INTERVAL '1 day') THEN
    -- Jika iya, mengizinkan penghapusan
    RETURN OLD;
  ELSE
    -- Jika tidak, menolak penghapusan dan menampilkan pesan error
    RAISE EXCEPTION 'Tayangan tidak dapat dihapus karena belum terunduh lebih dari 1 hari.';
  END IF;
END;
$$
LANGUAGE plpgsql;


CREATE TRIGGER check_download_before_delete
BEFORE DELETE
ON PacilFlix."TAYANGAN_TERUNDUH"
FOR EACH ROW
EXECUTE FUNCTION check_download_duration();