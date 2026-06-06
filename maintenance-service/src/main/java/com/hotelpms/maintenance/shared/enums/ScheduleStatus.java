package com.hotelpms.maintenance.shared.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Status for a preventive maintenance schedule.
 */
@Getter
@AllArgsConstructor
public enum ScheduleStatus {
    ACTIVE("ACTIVE"),
    PAUSED("PAUSED"),
    COMPLETED("COMPLETED");

    private final String value;
}