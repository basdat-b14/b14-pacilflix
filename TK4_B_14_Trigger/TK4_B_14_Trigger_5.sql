CREATE OR REPLACE FUNCTION handle_subscription()
RETURNS TRIGGER AS $$
DECLARE
    existing_subscription RECORD;
BEGIN
    -- cek active subscription yang ada 
    SELECT * INTO existing_subscription
    FROM "PacilFlix"."TRANSACTIONS"
    WHERE "username" = NEW."username"
    AND "end_date_time" > CURRENT_TIMESTAMP
    ORDER BY "end_date_time" DESC
    LIMIT 1;

    IF FOUND THEN
        -- mengupdate active subscriptions dengan yang baru
        UPDATE "PacilFlix"."TRANSACTIONS"
        SET "start_date_time" = NEW."start_date_time",
            "end_date_time" = NEW."end_date_time",
            "nama_paket" = NEW."nama_paket",
            "metode_pembayaran" = NEW."metode_pembayaran",
            "timestamp_pembayaran" = NEW."timestamp_pembayaran"
        WHERE "username" = existing_subscription."username"
        AND "start_date_time" = existing_subscription."start_date_time";
        -- Skip insert karena sudah melakukan update
        RETURN NULL;
    ELSE
        -- Melakukan insert jika tidak ada paket aktif
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER subscription_trigger
BEFORE INSERT ON "PacilFlix"."TRANSACTIONS"
FOR EACH ROW
EXECUTE FUNCTION handle_subscription();
