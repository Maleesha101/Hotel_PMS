package com.hotelpms.maintenance.shared.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Priority levels used across complaints and maintenance requests.
 */
@Getter
@AllArgsConstructor
public enum Priority {
    LOW("LOW"),
    MEDIUM("MEDIUM"),
    HIGH("HIGH"),
    CRITICAL("CRITICAL");

    private final String value;
}