package com.hotelpms.maintenance.domain.equipment.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.PositiveOrZero;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * DTO for adding a service‑history record to an existing piece of equipment.
 */
@Data
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
}
