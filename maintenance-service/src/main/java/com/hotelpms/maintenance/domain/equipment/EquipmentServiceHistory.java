package com.hotelpms.maintenance.domain.equipment;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

/**
 * JPA entity representing a service history record for a piece of equipment.
 */
@Entity
@Table(name = "equipment_service_history")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class EquipmentServiceHistory {

    @Id
    @GeneratedValue
    private UUID id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "equipment_id", nullable = false)
    private Equipment equipment;

    @Column(name = "service_date", nullable = false)
    private Instant serviceDate;

    @Column(name = "service_type", nullable = false, length = 100)
    private String serviceType;

    @Column(name = "performed_by", length = 100)
    private String performedBy;

    @Column(name = "cost", precision = 10, scale = 2)
    private BigDecimal cost;

    @Column(name = "notes", columnDefinition = "TEXT")
    private String notes;

    @Column(name = "next_service_date")
    private java.sql.Date nextServiceDate;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private Instant createdAt;
}
