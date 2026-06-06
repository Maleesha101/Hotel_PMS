package com.hotelpms.maintenance.domain.complaint.dto;

import com.hotelpms.maintenance.shared.enums.ComplaintCategory;
import com.hotelpms.maintenance.shared.enums.Priority;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.util.List;

/**
 * DTO for creating a new complaint.
 */
public class CreateComplaintRequest {

    @NotBlank
    @Size(max = 255)
    private String guestName;

    @NotBlank
    @Size(max = 50)
    private String roomId;

    @Size(max = 100)
    private String bookingRef;

    @NotNull
    private ComplaintCategory category;

    @NotBlank
    private String description;

    @NotNull
    private Priority urgency;

    @NotBlank
    @Size(max = 100)
    private String recordedBy;

    private List<@NotBlank String> photoUrls;

    // Getters and setters (or Lombok, but keep explicit for clarity)
    public String getGuestName() { return guestName; }
    public void setGuestName(String guestName) { this.guestName = guestName; }
    public String getRoomId() { return roomId; }
    public void setRoomId(String roomId) { this.roomId = roomId; }
    public String getBookingRef() { return bookingRef; }
    public void setBookingRef(String bookingRef) { this.bookingRef = bookingRef; }
    public ComplaintCategory getCategory() { return category; }
    public void setCategory(ComplaintCategory category) { this.category = category; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public Priority getUrgency() { return urgency; }
    public void setUrgency(Priority urgency) { this.urgency = urgency; }
    public String getRecordedBy() { return recordedBy; }
    public void setRecordedBy(String recordedBy) { this.recordedBy = recordedBy; }
    public List<String> getPhotoUrls() { return photoUrls; }
    public void setPhotoUrls(List<String> photoUrls) { this.photoUrls = photoUrls; }
}