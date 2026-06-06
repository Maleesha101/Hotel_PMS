package com.hotelpms.maintenance.shared.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Status for a maintenance request.
 */
@Getter
@AllArgsConstructor
public enum MaintenanceStatus {
    PENDING("PENDING"),
    ASSIGNED("ASSIGNED"),
    IN_PROGRESS("IN_PROGRESS"),
    WAITING_FOR_PARTS("WAITING_FOR_PARTS"),
    COMPLETED("COMPLETED"),
    CANCELLED("CANCELLED");

    private final String value;
}