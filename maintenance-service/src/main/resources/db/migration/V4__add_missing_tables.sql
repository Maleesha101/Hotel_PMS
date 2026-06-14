-- Child tables backing JPA @ElementCollection mappings

-- Complaint.photoUrls
CREATE TABLE IF NOT EXISTS complaint_photos (
                                                complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    url          VARCHAR(255)
    );
CREATE INDEX IF NOT EXISTS idx_complaint_photos_complaint_id
    ON complaint_photos(complaint_id);

-- MaintenanceRequest.partsUsed
CREATE TABLE IF NOT EXISTS maintenance_request_parts (
                                                         request_id UUID NOT NULL REFERENCES maintenance_requests(id) ON DELETE CASCADE,
    part       VARCHAR(255)
    );
CREATE INDEX IF NOT EXISTS idx_mr_parts_request_id
    ON maintenance_request_parts(request_id);

-- MaintenanceRequest.photoUrls
CREATE TABLE IF NOT EXISTS maintenance_request_photos (
                                                          request_id UUID NOT NULL REFERENCES maintenance_requests(id) ON DELETE CASCADE,
    url        VARCHAR(255)
    );
CREATE INDEX IF NOT EXISTS idx_mr_photos_request_id
    ON maintenance_request_photos(request_id);

-- The old inline TEXT[] columns on the parent tables are no longer used by JPA.
-- Drop them so the schema reflects the actual mapping (safe because nothing has run yet in dev).
ALTER TABLE complaints           DROP COLUMN IF EXISTS photo_urls;
ALTER TABLE maintenance_requests DROP COLUMN IF EXISTS parts_used;
ALTER TABLE maintenance_requests DROP COLUMN IF EXISTS photo_urls;