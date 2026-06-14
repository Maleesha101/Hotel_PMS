package com.hotelpms.maintenance.config;

import com.hotelpms.maintenance.shared.exception.InvalidStateException;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.security.KeyFactory;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.X509EncodedKeySpec;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

/**
 * JWT authentication filter that validates RS256 tokens using the public key supplied via
 * {@code jwt.public-key} property. On success it populates the Spring Security context with the
 * user id (subject) and roles (authorities).
 */
@Slf4j
@Component
public class JwtAuthFilter extends OncePerRequestFilter {

    @Value("${jwt.public-key:}")
    private String publicKeyPem;

    private static final String BEARER_PREFIX = "Bearer ";
    private volatile PublicKey cachedPublicKey;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {
        try {
            String header = request.getHeader(HttpHeaders.AUTHORIZATION);
            if (StringUtils.hasText(header) && header.startsWith(BEARER_PREFIX)) {
                String token = header.substring(BEARER_PREFIX.length());
                Claims claims = parseToken(token);
                String subject = claims.getSubject();
                @SuppressWarnings("unchecked")
                List<String> roles = claims.get("roles", List.class);
                List<SimpleGrantedAuthority> authorities = roles != null ?
                        roles.stream().map(r -> new SimpleGrantedAuthority("ROLE_" + r)).collect(Collectors.toList())
                        : Collections.emptyList();
                UsernamePasswordAuthenticationToken authentication =
                        new UsernamePasswordAuthenticationToken(subject, null, authorities);
                SecurityContextHolder.getContext().setAuthentication(authentication);
            }
        } catch (Exception ex) {
            log.warn("JWT validation failed: {}", ex.getMessage());
            // In case of token failure, we do not set authentication – downstream will reject unauthenticated.
        }
        filterChain.doFilter(request, response);
    }

    private Claims parseToken(String token) {
        if (!StringUtils.hasText(publicKeyPem)) { // Ensure public key is configured
            throw new InvalidStateException("JWT public key is not configured");
        }

        if (cachedPublicKey == null) { // Cache the public key to avoid re-parsing on every request
            synchronized (this) {
                if (cachedPublicKey == null) {
                    try {
                        // Remove PEM header/footer and whitespace
                        String cleaned = publicKeyPem
                                .replaceAll("-----BEGIN PUBLIC KEY-----", "")
                                .replaceAll("-----END PUBLIC KEY-----", "")
                                .replaceAll("\\s", "");
                        byte[] keyBytes = java.util.Base64.getDecoder().decode(cleaned);
                        
                        // Create RSA public key from bytes
                        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
                        X509EncodedKeySpec keySpec = new X509EncodedKeySpec(keyBytes);
                        cachedPublicKey = keyFactory.generatePublic(keySpec);
                    } catch (NoSuchAlgorithmException e) {
                throw new InvalidStateException("RSA algorithm not found for public key parsing");
                    } catch (InvalidKeySpecException e) {
                throw new InvalidStateException("Invalid public key spec for RSA public key parsing. Ensure it's a valid X.509 PEM format.");
                    }
                }
            }
        }
        
        return Jwts.parserBuilder()
                .setSigningKey(cachedPublicKey) // Use the actual RSA public key here
                .build()
                .parseClaimsJws(token)
                .getBody();
    }
}
