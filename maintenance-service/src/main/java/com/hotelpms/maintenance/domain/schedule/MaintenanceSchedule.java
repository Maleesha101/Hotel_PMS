package com.hotelpms.maintenance.domain.schedule;

import com.hotelpms.maintenance.shared.enums.ScheduleStatus;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.Date;
import java.util.UUID;

/**
 * JPA entity representing a preventive maintenance schedule for a piece of equipment.
 */
@Entity
@Table(name = "maintenance_schedules")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class MaintenanceSchedule {

    @Id
    @GeneratedValue
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "equipment_id")
    private com.hotelpms.maintenance.domain.equipment.Equipment equipment;

    @Column(name = "schedule_name", nullable = false, length = 255)
    private String scheduleName;

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Column(name = "frequency_days", nullable = false)
    private Integer frequencyDays;

    @Column(name = "last_run_date")
    private Date lastRunDate;

    @Column(name = "next_due_date", nullable = false)
    private Date nextDueDate;

    @Column(name = "assigned_technician", length = 100)
    private String assignedTechnician;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 20)
    private ScheduleStatus status;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private Instant updatedAt;
}
