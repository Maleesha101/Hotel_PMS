package com.hotelpms.maintenance.shared.enums;

/**
 * Types of equipment tracked by the service.
 */
public enum EquipmentType {
    AC("AC"),
    TV("TV"),
    WATER_HEATER("WATER_HEATER"),
    FRIDGE("FRIDGE"),
    GENERATOR("GENERATOR"),
    ELEVATOR("ELEVATOR"),
    OTHER("OTHER");

    private final String value;

    EquipmentType(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }
}