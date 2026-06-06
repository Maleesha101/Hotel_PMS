package com.hotelpms.maintenance.domain.complaint;

import com.hotelpms.maintenance.shared.enums.ComplaintCategory;
import com.hotelpms.maintenance.shared.enums.ComplaintStatus;
import com.hotelpms.maintenance.shared.enums.Priority;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

/**
 * JPA entity representing a guest complaint.
 */
@Entity
@Table(name = "complaints")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Complaint {

    @Id
    @GeneratedValue
    private UUID id;

    @Column(name = "guest_name", nullable = false, length = 255)
    private String guestName;

    @Column(name = "room_id", nullable = false, length = 50)
    private String roomId;

    @Column(name = "booking_ref", length = 100)
    private String bookingRef;

    @Column(name = "complaint_date", nullable = false, updatable = false)
    private Instant complaintDate;

    @Enumerated(EnumType.STRING)
    @Column(name = "category", nullable = false, length = 100)
    private ComplaintCategory category;

    @Column(name = "description", nullable = false, columnDefinition = "TEXT")
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(name = "urgency", nullable = false, length = 20)
    private Priority urgency;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 30)
    private ComplaintStatus status;

    @Column(name = "recorded_by", nullable = false, length = 100)
    private String recordedBy;

    @Column(name = "maintenance_request_id")
    private UUID maintenanceRequestId;

    @Column(name = "resolution_notes", columnDefinition = "TEXT")
    private String resolutionNotes;

    @ElementCollection
    @CollectionTable(name = "complaint_photos", joinColumns = @JoinColumn(name = "complaint_id"))
    @Column(name = "url")
    private List<String> photoUrls;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private Instant updatedAt;
}
