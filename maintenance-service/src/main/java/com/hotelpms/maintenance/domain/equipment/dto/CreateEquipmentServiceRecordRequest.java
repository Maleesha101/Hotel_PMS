package com.hotelpms.maintenance.domain.equipment.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;
import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * DTO for adding a service‑history record to an existing piece of equipment.
 */
public class CreateEquipmentServiceRecordRequest {

    @NotNull
    private LocalDate serviceDate;

    @NotBlank
    private String serviceType;

    private String performedBy;

    @PositiveOrZero
    private BigDecimal cost;

    private String notes;

    private LocalDate nextServiceDate;

    // getters / setters
    public LocalDate getServiceDate() { return serviceDate; }
    public void setServiceDate(LocalDate serviceDate) { this.serviceDate = serviceDate; }
    public String getServiceType() { return serviceType; }
    public void setServiceType(String serviceType) { this.serviceType = serviceType; }
    public String getPerformedBy() { return performedBy; }
    public void setPerformedBy(String performedBy) { this.performedBy = performedBy; }
    public BigDecimal getCost() { return cost; }
    public void setCost(BigDecimal cost) { this.cost = cost; }
    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
    public LocalDate getNextServiceDate() { return nextServiceDate; }
    public void setNextServiceDate(LocalDate nextServiceDate) { this.nextServiceDate = nextServiceDate; }
}
