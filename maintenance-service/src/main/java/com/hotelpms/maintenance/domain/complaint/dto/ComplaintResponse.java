package com.hotelpms.maintenance.domain.complaint.dto;

import com.hotelpms.maintenance.shared.enums.ComplaintCategory;
import com.hotelpms.maintenance.shared.enums.ComplaintStatus;
import com.hotelpms.maintenance.shared.enums.Priority;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

/**
 * DTO representing a complaint returned from the API.
 */
@Schema(description = "Complaint response payload")
@Data
public class ComplaintResponse {

    @Schema(description = "Unique identifier of the complaint", example = "123e4567-e89b-12d3-a456-426614174000")
    private UUID id;

    @Schema(description = "Name of the guest who filed the complaint")
    private String guestName;

    @Schema(description = "Room identifier")
    private String roomId;

    @Schema(description = "Booking reference, if any")
    private String bookingRef;

    @Schema(description = "Date and time when the complaint was recorded")
    private Instant complaintDate;

    @Schema(description = "Category of the complaint")
    private ComplaintCategory category;

    @Schema(description = "Detailed description of the issue")
    private String description;

    @Schema(description = "Urgency level of the complaint")
    private Priority urgency;

    @Schema(description = "Current status of the complaint")
    private ComplaintStatus status;

    @Schema(description = "User ID of the staff member who recorded the complaint")
    private String recordedBy;

    @Schema(description = "Resolution notes, if the complaint has been addressed")
    private String resolutionNotes;

    @Schema(description = "List of photo URLs attached to the complaint")
    private List<String> photoUrls;

    @Schema(description = "Timestamp when the record was created")
    private Instant createdAt;

    @Schema(description = "Timestamp when the record was last updated")
    private Instant updatedAt;
}