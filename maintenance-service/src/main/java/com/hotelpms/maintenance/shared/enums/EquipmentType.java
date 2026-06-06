package com.hotelpms.maintenance.shared.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Types of equipment tracked by the service.
 */
@Getter
@AllArgsConstructor
public enum EquipmentType {
    AC("AC"),
    TV("TV"),
    WATER_HEATER("WATER_HEATER"),
    FRIDGE("FRIDGE"),
    GENERATOR("GENERATOR"),
    ELEVATOR("ELEVATOR"),
    OTHER("OTHER");

    private final String value;
}