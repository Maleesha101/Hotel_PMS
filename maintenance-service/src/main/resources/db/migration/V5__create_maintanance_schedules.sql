CREATE TABLE IF NOT EXISTS maintenance_schedules (
                                                     id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    equipment_id        UUID REFERENCES equipment(id) ON DELETE SET NULL,
    schedule_name       VARCHAR(255) NOT NULL,
    description         TEXT,
    frequency_days      INTEGER      NOT NULL,
    last_run_date       DATE,
    next_due_date       DATE         NOT NULL,
    assigned_technician VARCHAR(100),
    status              VARCHAR(20)  NOT NULL DEFAULT 'ACTIVE',
    created_at          TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

CREATE INDEX IF NOT EXISTS idx_ms_equipment_id ON maintenance_schedules(equipment_id);
CREATE INDEX IF NOT EXISTS idx_ms_status       ON maintenance_schedules(status);
CREATE INDEX IF NOT EXISTS idx_ms_next_due     ON maintenance_schedules(next_due_date);