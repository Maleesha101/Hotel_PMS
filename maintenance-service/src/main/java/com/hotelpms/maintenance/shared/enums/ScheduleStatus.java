package com.hotelpms.maintenance.shared.enums;

/**
 * Status for a preventive maintenance schedule.
 */
public enum ScheduleStatus {
    ACTIVE("ACTIVE"),
    PAUSED("PAUSED"),
    COMPLETED("COMPLETED");

    private final String value;

    ScheduleStatus(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }
}