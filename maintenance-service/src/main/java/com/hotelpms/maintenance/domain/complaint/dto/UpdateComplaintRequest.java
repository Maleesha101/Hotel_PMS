package com.hotelpms.maintenance.domain.complaint.dto;

import com.hotelpms.maintenance.shared.enums.ComplaintStatus;
import jakarta.validation.constraints.Size;

/**
 * DTO for updating mutable fields of a complaint.
 */
public class UpdateComplaintRequest {

    private ComplaintStatus status;

    @Size(max = 5000)
    private String resolutionNotes;

    // Getters and setters
    public ComplaintStatus getStatus() { return status; }
    public void setStatus(ComplaintStatus status) { this.status = status; }
    public String getResolutionNotes() { return resolutionNotes; }
    public void setResolutionNotes(String resolutionNotes) { this.resolutionNotes = resolutionNotes; }
}