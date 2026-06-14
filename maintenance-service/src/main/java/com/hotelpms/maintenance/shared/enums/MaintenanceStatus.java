
package com.hotelpms.maintenance.shared.enums;

/**
 * Status for a maintenance request.
 */
public enum MaintenanceStatus {
    PENDING("PENDING"),
    ASSIGNED("ASSIGNED"),
    IN_PROGRESS("IN_PROGRESS"),
    WAITING_FOR_PARTS("WAITING_FOR_PARTS"),
    COMPLETED("COMPLETED"),
    CANCELLED("CANCELLED");

    private final String value;

    MaintenanceStatus(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }
}