package com.hotelpms.maintenance.domain.request.dto;

import com.hotelpms.maintenance.shared.enums.MaintenanceStatus;
import com.hotelpms.maintenance.shared.enums.Priority;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.time.Instant;
import java.util.UUID;

@Data
@Schema(description = "Maintenance request response")
public class MaintenanceRequestResponse {
    private UUID id;
    private String roomId;
    private String description;
    private Priority priority;
    private MaintenanceStatus status;
    private String assignedTechnician;
    private Instant createdAt;
    private Instant updatedAt;
    private Instant completedAt;
    private String completionNotes;
}