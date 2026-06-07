package com.hotelpms.maintenance.domain.request.dto;

import com.hotelpms.maintenance.shared.enums.MaintenanceStatus;
import com.hotelpms.maintenance.shared.enums.Priority;
import jakarta.validation.constraints.Size;
import java.math.BigDecimal;
import java.util.List;

/**
 * DTO for updating mutable fields of a maintenance request.
 */
public class UpdateMaintenanceRequest {

    private String assignedTechnician;

    private MaintenanceStatus status;

    private Priority priority;

    private BigDecimal estimatedCost;

    private BigDecimal actualCost;

    private String completionNotes;

    private List<@Size(max = 255) String> partsUsed;

    // Getters and setters
    public String getAssignedTechnician() { return assignedTechnician; }
    public void setAssignedTechnician(String assignedTechnician) { this.assignedTechnician = assignedTechnician; }
    public MaintenanceStatus getStatus() { return status; }
    public void setStatus(MaintenanceStatus status) { this.status = status; }
    public Priority getPriority() { return priority; }
    public void setPriority(Priority priority) { this.priority = priority; }
    public BigDecimal getEstimatedCost() { return estimatedCost; }
    public void setEstimatedCost(BigDecimal estimatedCost) { this.estimatedCost = estimatedCost; }
    public BigDecimal getActualCost() { return actualCost; }
    public void setActualCost(BigDecimal actualCost) { this.actualCost = actualCost; }
    public String getCompletionNotes() { return completionNotes; }
    public void setCompletionNotes(String completionNotes) { this.completionNotes = completionNotes; }
    public List<String> getPartsUsed() { return partsUsed; }
    public void setPartsUsed(List<String> partsUsed) { this.partsUsed = partsUsed; }
}
