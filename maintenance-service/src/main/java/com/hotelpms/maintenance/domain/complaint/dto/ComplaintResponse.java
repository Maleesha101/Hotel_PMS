package com.hotelpms.maintenance.domain.complaint.dto;

import com.hotelpms.maintenance.shared.enums.ComplaintCategory;
import com.hotelpms.maintenance.shared.enums.ComplaintStatus;
import com.hotelpms.maintenance.shared.enums.Priority;
import io.swagger.v3.oas.annotations.media.Schema;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

/**
 * DTO representing a complaint returned from the API.
 */
@Schema(description = "Complaint response payload")
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

    // Getters and setters
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public String getGuestName() { return guestName; }
    public void setGuestName(String guestName) { this.guestName = guestName; }
    public String getRoomId() { return roomId; }
    public void setRoomId(String roomId) { this.roomId = roomId; }
    public String getBookingRef() { return bookingRef; }
    public void setBookingRef(String bookingRef) { this.bookingRef = bookingRef; }
    public Instant getComplaintDate() { return complaintDate; }
    public void setComplaintDate(Instant complaintDate) { this.complaintDate = complaintDate; }
    public ComplaintCategory getCategory() { return category; }
    public void setCategory(ComplaintCategory category) { this.category = category; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public Priority getUrgency() { return urgency; }
    public void setUrgency(Priority urgency) { this.urgency = urgency; }
    public ComplaintStatus getStatus() { return status; }
    public void setStatus(ComplaintStatus status) { this.status = status; }
    public String getRecordedBy() { return recordedBy; }
    public void setRecordedBy(String recordedBy) { this.recordedBy = recordedBy; }
    public String getResolutionNotes() { return resolutionNotes; }
    public void setResolutionNotes(String resolutionNotes) { this.resolutionNotes = resolutionNotes; }
    public List<String> getPhotoUrls() { return photoUrls; }
    public void setPhotoUrls(List<String> photoUrls) { this.photoUrls = photoUrls; }
    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
    public Instant getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Instant updatedAt) { this.updatedAt = updatedAt; }
}