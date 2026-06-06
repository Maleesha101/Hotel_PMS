package com.hotelpms.maintenance.domain.equipment;

import com.hotelpms.maintenance.shared.enums.EquipmentType;
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
 * JPA entity representing a piece of equipment owned by the hotel.
 */
@Entity
@Table(name = "equipment")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Equipment {

    @Id
    @GeneratedValue
    private UUID id;

    @Column(name = "name", nullable = false, length = 255)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(name = "equipment_type", nullable = false, length = 100)
    private EquipmentType equipmentType;

    @Column(name = "serial_number", length = 100)
    private String serialNumber;

    @Column(name = "location", nullable = false, length = 255)
    private String location;

    @Column(name = "purchase_date")
    private java.sql.Date purchaseDate;

    @Column(name = "warranty_expiry")
    private java.sql.Date warrantyExpiry;

    @Column(name = "last_service_date")
    private java.sql.Date lastServiceDate;

    @Column(name = "next_service_date")
    private java.sql.Date nextServiceDate;

    @Column(name = "status", nullable = false, length = 30)
    private String status; // Could be an enum, but kept as String for flexibility

    @Column(name = "notes", columnDefinition = "TEXT")
    private String notes;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private Instant updatedAt;

    // One equipment can have many service history records
    @OneToMany(mappedBy = "equipment", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<EquipmentServiceHistory> serviceHistory;
}
