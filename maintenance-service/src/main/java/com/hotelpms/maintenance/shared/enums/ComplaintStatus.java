package com.hotelpms.maintenance.shared.enums;

/**
 * Statuses for a guest complaint.
 */
public enum ComplaintStatus {
    OPEN("OPEN"),
    IN_REVIEW("IN_REVIEW"),
    FORWARDED_TO_MAINTENANCE("FORWARDED_TO_MAINTENANCE"),
    RESOLVED("RESOLVED"),
    CLOSED("CLOSED");

    private final String value;

    ComplaintStatus(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }
}