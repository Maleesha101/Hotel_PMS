package com.hotelpms.maintenance;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * Entry point for the Hotel PMS Maintenance Service.
 */
@SpringBootApplication
@EnableScheduling
public class MaintenanceServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(MaintenanceServiceApplication.class, args);
    }
}
