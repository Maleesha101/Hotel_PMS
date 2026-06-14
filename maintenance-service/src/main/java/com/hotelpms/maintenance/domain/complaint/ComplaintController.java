package com.hotelpms.maintenance.domain.complaint;

import com.hotelpms.maintenance.domain.complaint.dto.*;
import com.hotelpms.maintenance.domain.complaint.mapper.ComplaintMapper;
import com.hotelpms.maintenance.shared.enums.ComplaintStatus;
import com.hotelpms.maintenance.shared.enums.Priority;
import com.hotelpms.maintenance.shared.response.ApiResponse;
import com.hotelpms.maintenance.shared.response.PagedResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

/**
 * REST controller for complaint management.
 */
@RestController
@RequestMapping("/api/v1/complaints")
@RequiredArgsConstructor
@Tag(name = "Complaints", description = "Endpoints for managing guest complaints")
public class ComplaintController {

    private final ComplaintService complaintService;
    private final ComplaintMapper mapper;

    @PostMapping
    @Operation(summary = "Record a new complaint")
    @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "201", description = "Complaint created")
    public ResponseEntity<ApiResponse<Void>> createComplaint(@Valid @RequestBody CreateComplaintRequest request) {
        complaintService.createComplaint(request);
        return ResponseEntity.status(201).body(new ApiResponse<>(201, "Complaint created", null));
    }

    @GetMapping
    @Transactional(readOnly = true)
    @Operation(summary = "List complaints with optional filters")
    @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "List of complaints")
    public ResponseEntity<ApiResponse<PagedResponse<ComplaintResponse>>> listComplaints(
            @RequestParam(name = "roomId", required = false) String roomId,
            @RequestParam(name = "bookingRef", required = false) String bookingRef,
            @RequestParam(name = "urgency", required = false) Priority urgency,
            @RequestParam(name = "status", required = false) ComplaintStatus status,
            @RequestParam(name = "page", defaultValue = "0") int page,
            @RequestParam(name = "size", defaultValue = "20") int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<Complaint> entities;
        if (roomId != null) {
            entities = complaintService.findByRoomId(roomId, pageable);
        } else if (bookingRef != null) {
            entities = complaintService.findByBookingRef(bookingRef, pageable);
        } else if (urgency != null) {
            entities = complaintService.findByUrgency(urgency, pageable);
        } else if (status != null) {
            entities = complaintService.findByStatus(status, pageable);
        } else {
            entities = complaintService.findAll(pageable);
        }
        Page<ComplaintResponse> responses = entities.map(mapper::toResponse);
        return ResponseEntity.ok(new ApiResponse<>(200, "Complaints retrieved", PagedResponse.from(responses)));
    }

    @GetMapping("/{id}")
    @Transactional(readOnly = true)
    @Operation(summary = "Get a complaint by its UUID")
    @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Complaint details")
    public ResponseEntity<ApiResponse<ComplaintResponse>> getComplaint(@PathVariable UUID id) {
        ComplaintResponse response = complaintService.getById(id);
        return ResponseEntity.ok(new ApiResponse<>(200, "Complaint retrieved", response));
    }

    @PatchMapping("/{id}")
    @Operation(summary = "Update mutable fields of a complaint (status, resolution notes)")
    @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Complaint updated")
    public ResponseEntity<ApiResponse<ComplaintResponse>> updateComplaint(
            @PathVariable UUID id,
            @Valid @RequestBody UpdateComplaintRequest request) {
        ComplaintResponse response = complaintService.updateComplaint(id, request);
        return ResponseEntity.ok(new ApiResponse<>(200, "Complaint updated", response));
    }

    @PostMapping("/{id}/forward")
    @Operation(summary = "Forward a complaint to maintenance – creates a linked MaintenanceRequest")
    @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Complaint forwarded")
    public ResponseEntity<ApiResponse<Void>> forwardComplaint(@PathVariable UUID id,
                                                              org.springframework.security.core.Authentication authentication) {
        complaintService.forwardComplaint(id, authentication.getName());
        return ResponseEntity.ok(new ApiResponse<>(200, "Complaint forwarded to maintenance", null));
    }
}
