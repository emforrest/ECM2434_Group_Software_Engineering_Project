DELIMITER $$
CREATE EVENT `Every_1_Hour_Cleanup`
	ON SCHEDULE EVERY 60 MINUTE STARTS '2015-09-01 00:00:00'
	ON COMPLETION PRESERVE
DO BEGIN
	UPDATE user_journey
    SET origin_id=null
	WHERE TIMESTAMPDIFF(HOUR, time_finished, now()) > 336 AND NOT(SELECT on_campus FROM main_location WHERE id=origin_id);
    
    UPDATE user_journey
    SET destination_id=null
	WHERE TIMESTAMPDIFF(HOUR, time_finished, now()) > 336 AND NOT(SELECT on_campus FROM main_location WHERE id=destination_id);
END;$$
DELIMITER ;