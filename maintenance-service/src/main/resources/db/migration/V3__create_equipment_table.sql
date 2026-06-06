CREATE TABLE equipment (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name              VARCHAR(255) NOT NULL,
    equipment_type    VARCHAR(100) NOT NULL,
    serial_number     VARCHAR(100),
    location          VARCHAR(255) NOT NULL,
    purchase_date     DATE,
    warranty_expiry   DATE,
    last_service_date DATE,
    next_service_date DATE,
    status            VARCHAR(30) NOT NULL DEFAULT 'OPERATIONAL',
    notes             TEXT,
    created_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE equipment_service_history (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    equipment_id      UUID NOT NULL REFERENCES equipment(id) ON DELETE CASCADE,
    service_date      TIMESTAMP NOT NULL,
    service_type      VARCHAR(100) NOT NULL,
    performed_by      VARCHAR(100),
    cost              NUMERIC(10,2),
    notes             TEXT,
    next_service_date DATE,
    created_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_equipment_type ON equipment(equipment_type);
CREATE INDEX idx_equipment_location ON equipment(location);
CREATE INDEX idx_service_history ON equipment_service_history(equipment_id);
