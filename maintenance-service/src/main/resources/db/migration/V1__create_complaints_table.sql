CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE complaints (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_name      VARCHAR(255) NOT NULL,
    room_id         VARCHAR(50)  NOT NULL,
    booking_ref     VARCHAR(100),
    complaint_date  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    category        VARCHAR(100) NOT NULL, -- enum values defined in code
    description     TEXT         NOT NULL,
    urgency         VARCHAR(20)  NOT NULL, -- enum: LOW, MEDIUM, HIGH, CRITICAL
    status          VARCHAR(30)  NOT NULL DEFAULT 'OPEN', -- OPEN, IN_REVIEW, FORWARDED_TO_MAINTENANCE, RESOLVED, CLOSED
    recorded_by     VARCHAR(100) NOT NULL,
    maintenance_request_id UUID,
    resolution_notes TEXT,
    photo_urls      TEXT[],
    created_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_complaints_room_id ON complaints(room_id);
CREATE INDEX idx_complaints_status ON complaints(status);
CREATE INDEX idx_complaints_booking ON complaints(booking_ref);
