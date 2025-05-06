-- Проверяем существование колонки totalamount и добавляем её, если отсутствует
DO $$
BEGIN
    -- Проверяем, существует ли колонка totalamount в таблице bookings
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'bookings' AND column_name = 'totalamount'
    ) THEN
        -- Если колонки нет, добавляем её
        EXECUTE 'ALTER TABLE bookings ADD COLUMN totalamount DECIMAL(10, 2)';
        
        -- Обновляем значения totalamount на основе категории номера и длительности проживания
        EXECUTE '
            UPDATE bookings b
            SET totalamount = (
                SELECT rc.baseprice * (EXTRACT(DAY FROM (b.checkoutdate - b.checkindate)))
                FROM roomcategories rc
                WHERE rc.categoryid = b.categoryid
            )
            WHERE b.totalamount IS NULL';
            
        RAISE NOTICE 'Колонка totalamount успешно добавлена и заполнена!';
    ELSE
        RAISE NOTICE 'Колонка totalamount уже существует в таблице bookings.';
    END IF;
END $$; 