package com.hotelpms.maintenance.shared.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Statuses for a guest complaint.
 */
@Getter
@AllArgsConstructor
public enum ComplaintStatus {
    OPEN("OPEN"),
    IN_REVIEW("IN_REVIEW"),
    FORWARDED_TO_MAINTENANCE("FORWARDED_TO_MAINTENANCE"),
    RESOLVED("RESOLVED"),
    CLOSED("CLOSED");

    private final String value;
}