package com.hotelpms.maintenance.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.authorization.AuthorizationDecision;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

/**
 * Security configuration for the Maintenance Service.
 * <p>
 * All endpoints require a valid JWT (RS256). Role‑based access is enforced via antMatchers.
 * Swagger UI is disabled in the {@code prod} profile.
 */
@Configuration
@EnableMethodSecurity
public class SecurityConfig {

    @Value("${spring.profiles.active:dev}")
    private String activeProfile;

    private final JwtAuthFilter jwtAuthFilter;

    public SecurityConfig(JwtAuthFilter jwtAuthFilter) {
        this.jwtAuthFilter = jwtAuthFilter;
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // Disable CSRF for stateless APIs
            .csrf(csrf -> csrf.disable())
            // Stateless session management
            .sessionManagement(sess -> sess.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            // Exception handling delegated to GlobalExceptionHandler (Spring will pick it up)
            .exceptionHandling(Customizer.withDefaults())
            // Authorize requests
            .authorizeHttpRequests(auth -> auth
                // Swagger UI and API Docs – only enabled in dev profile
                .requestMatchers("/swagger-ui/**", "/v3/api-docs/**", "/v3/api-docs", "/swagger-ui.html").access((authentication, context) -> 
                    new AuthorizationDecision(!"prod".equalsIgnoreCase(activeProfile))
                )
                // Public health endpoints
                .requestMatchers(HttpMethod.GET, "/actuator/health", "/actuator/info").permitAll()
                    // Front Desk can create and read complaints
                    .requestMatchers(HttpMethod.POST, "/api/v1/complaints").hasAnyRole("ADMIN", "FRONT_DESK")
                    .requestMatchers(HttpMethod.GET, "/api/v1/complaints", "/api/v1/complaints/**").hasAnyRole("ADMIN", "FRONT_DESK", "HOUSEKEEPING")
                    // Maintenance staff can manage requests, equipment, schedules
                    .requestMatchers("/api/v1/requests/**", "/api/v1/equipment/**", "/api/v1/schedules/**")
                    .hasAnyRole("ADMIN", "MAINTENANCE_STAFF")
                    // Any other request requires authentication
                    .anyRequest().authenticated()
            )
            // Add JWT filter before Spring Security's UsernamePasswordAuthenticationFilter
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    // AuthenticationManager bean required for some custom auth flows (not used now but kept for extensibility)
    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration authConfig) throws Exception {
        return authConfig.getAuthenticationManager();
    }
}