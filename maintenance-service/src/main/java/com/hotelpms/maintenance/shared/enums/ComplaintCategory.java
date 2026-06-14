package com.hotelpms.maintenance.shared.enums;

/**
 * Categories for a complaint.
 */
public enum ComplaintCategory {
    AC("AC"),
    PLUMBING("PLUMBING"),
    ELECTRICAL("ELECTRICAL"),
    CLEANLINESS("CLEANLINESS"),
    FURNITURE("FURNITURE"),
    NOISE("NOISE"),
    OTHER("OTHER");

    private final String value;

    ComplaintCategory(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }
}