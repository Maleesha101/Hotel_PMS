package com.hotelpms.maintenance.shared.enums;

/**
 * Priority levels used across complaints and maintenance requests.
 */
public enum Priority {
    LOW("LOW"),
    MEDIUM("MEDIUM"),
    HIGH("HIGH"),
    CRITICAL("CRITICAL");

    private final String value;

    Priority(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }
}