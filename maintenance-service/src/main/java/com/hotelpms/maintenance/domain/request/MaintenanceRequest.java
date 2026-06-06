package com.hotelpms.maintenance.domain.request;

import com.hotelpms.maintenance.shared.enums.MaintenanceStatus;
import com.hotelpms.maintenance.shared.enums.Priority;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

/**
 * JPA entity representing a maintenance request.
 */
@Entity
@Table(name = "maintenance_requests")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MaintenanceRequest {

    @Id
    @GeneratedValue
    private UUID id;

    @Column(name = "room_id", nullable = false, length = 50)
    private String roomId;

    @Column(name = "location_notes", length = 255)
    private String locationNotes;

    @Column(name = "issue_type", nullable = false, length = 100)
    private String issueType;

    @Column(name = "description", nullable = false, columnDefinition = "TEXT")
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(name = "priority", nullable = false, length = 20)
    private Priority priority;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 30)
    private MaintenanceStatus status;

    @Column(name = "reported_by", nullable = false, length = 100)
    private String reportedBy;

    @Column(name = "reported_date", nullable = false, updatable = false)
    private Instant reportedDate;

    @Column(name = "assigned_technician", length = 100)
    private String assignedTechnician;

    @Column(name = "estimated_cost", precision = 10, scale = 2)
    private BigDecimal estimatedCost;

    @Column(name = "actual_cost", precision = 10, scale = 2)
    private BigDecimal actualCost;

    @Column(name = "completion_notes", columnDefinition = "TEXT")
    private String completionNotes;

    @ElementCollection
    @CollectionTable(name = "maintenance_request_parts", joinColumns = @JoinColumn(name = "request_id"))
    @Column(name = "part")
    private List<String> partsUsed;

    @Column(name = "complaint_id")
    private UUID complaintId;

    @Column(name = "damage_report_id", length = 100)
    private String damageReportId;

    @Column(name = "is_guest_chargeable", nullable = false)
    private Boolean isGuestChargeable;

    @Column(name = "completed_at")
    private Instant completedAt;

    @ElementCollection
    @CollectionTable(name = "maintenance_request_photos", joinColumns = @JoinColumn(name = "request_id"))
    @Column(name = "url")
    private List<String> photoUrls;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private Instant updatedAt;
}
