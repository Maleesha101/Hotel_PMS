CREATE TABLE maintenance_requests (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id             VARCHAR(50)   NOT NULL,
    location_notes      VARCHAR(255),
    issue_type          VARCHAR(100)  NOT NULL,
    description         TEXT          NOT NULL,
    priority            VARCHAR(20)   NOT NULL DEFAULT 'MEDIUM',
    status              VARCHAR(30)   NOT NULL DEFAULT 'PENDING',
    reported_by         VARCHAR(100)  NOT NULL,
    reported_date       TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    assigned_technician VARCHAR(100),
    estimated_cost      NUMERIC(10,2),
    actual_cost         NUMERIC(10,2),
    completion_notes    TEXT,
    parts_used          TEXT[],
    complaint_id        UUID REFERENCES complaints(id),
    damage_report_id    VARCHAR(100),
    is_guest_chargeable BOOLEAN       NOT NULL DEFAULT FALSE,
    completed_at        TIMESTAMP,
    photo_urls          TEXT[],
    created_at          TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_mr_room_id   ON maintenance_requests(room_id);
CREATE INDEX idx_mr_status    ON maintenance_requests(status);
CREATE INDEX idx_mr_priority  ON maintenance_requests(priority);
CREATE INDEX idx_mr_technician ON maintenance_requests(assigned_technician);
