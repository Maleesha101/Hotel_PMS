package com.hotelpms.maintenance.domain.request.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class CompleteMaintenanceRequest {
    @NotBlank(message = "Completion notes are required")
    private String completionNotes;
}