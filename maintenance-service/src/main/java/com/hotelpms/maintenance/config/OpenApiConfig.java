package com.hotelpms.maintenance.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.OpenAPI;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * OpenAPI (Swagger) configuration for the Maintenance Service.
 * Provides API metadata, security scheme, and global settings.
 */
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI maintenanceServiceOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("Hotel PMS — Maintenance Service API")
                        .description("""
                                Manages maintenance requests, customer complaints, equipment records,
                                and preventive maintenance schedules for the Hotel Property Management System.

                                ## Authentication
                                All endpoints require a valid JWT Bearer token issued by the Auth Service.
                                Pass it in the `Authorization: Bearer <token>` header.

                                ## Event-Driven Integration
                                This service publishes to `hotel.maintenance.completed` and
                                `hotel.maintenance.charge-to-invoice` Kafka topics.
                                It consumes from `hotel.booking.checkout` and `hotel.housekeeping.damage-reported`.
                                """)
                        .version("1.0.0")
                        .contact(new Contact().name("Hotel PMS Team"))
                        .license(new License().name("Private")))
                .addSecurityItem(new SecurityRequirement().addList("BearerAuth"))
                .components(new Components()
                        .addSecuritySchemes("BearerAuth", new SecurityScheme()
                                .name("BearerAuth")
                                .type(SecurityScheme.Type.HTTP)
                                .scheme("bearer")
                                .bearerFormat("JWT")));
    }
}
