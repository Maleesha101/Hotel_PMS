-- Align column types with the JPA entity (java.util.Date without @Temporal -> TIMESTAMP)
ALTER TABLE maintenance_schedules
ALTER COLUMN last_run_date TYPE TIMESTAMP USING last_run_date::timestamp;

ALTER TABLE maintenance_schedules
ALTER COLUMN next_due_date TYPE TIMESTAMP USING next_due_date::timestamp;