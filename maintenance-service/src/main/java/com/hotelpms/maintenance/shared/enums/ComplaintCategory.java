package com.hotelpms.maintenance.shared.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Categories for a complaint.
 */
@Getter
@AllArgsConstructor
public enum ComplaintCategory {
    AC("AC"),
    PLUMBING("PLUMBING"),
    ELECTRICAL("ELECTRICAL"),
    CLEANLINESS("CLEANLINESS"),
    FURNITURE("FURNITURE"),
    NOISE("NOISE"),
    OTHER("OTHER");

    private final String value;
}