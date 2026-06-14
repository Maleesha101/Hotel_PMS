package com.hotelpms.maintenance.domain.request;

import com.hotelpms.maintenance.domain.request.dto.*;
import com.hotelpms.maintenance.domain.request.mapper.MaintenanceRequestMapper;
import com.hotelpms.maintenance.shared.enums.MaintenanceStatus;
import com.hotelpms.maintenance.shared.enums.Priority;
import com.hotelpms.maintenance.shared.exception.ResourceNotFoundException;
import com.hotelpms.maintenance.shared.response.ApiResponse;
import com.hotelpms.maintenance.shared.response.PagedResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.*;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

/**
 * REST controller for maintenance request management.
 */
@RestController
@RequestMapping("/api/v1/requests")
@RequiredArgsConstructor
@Tag(name = "Maintenance Requests", description = "Endpoints for handling maintenance requests")
public class MaintenanceRequestController {

    private final MaintenanceRequestService requestService;
    private final MaintenanceRequestMapper mapper;

    @PostMapping
    @Operation(summary = "Create a new maintenance request")
    @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "201", description = "Request created")
    public ResponseEntity<ApiResponse<MaintenanceRequestResponse>> createRequest(@Valid @RequestBody CreateMaintenanceRequest dto) {
        MaintenanceRequestResponse resp = requestService.createRequest(dto);
        return ResponseEntity.status(201).body(new ApiResponse<>(201, "Maintenance request created", resp));
    }

    @GetMapping
    @Operation(summary = "List maintenance requests with optional filters")
    @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "List of requests")
    public ResponseEntity<ApiResponse<PagedResponse<MaintenanceRequestResponse>>> listRequests(
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String roomId,
            @RequestParam(required = false) String priority,
            @RequestParam(required = false) String technician,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<MaintenanceRequest> entities;
        if (status != null) {
            entities = requestService.repository.findByStatus(MaintenanceStatus.valueOf(status), pageable);
        } else if (roomId != null) {
            entities = requestService.repository.findByRoomId(roomId, pageable);
        } else if (priority != null) {
            entities = requestService.repository.findByPriority(Priority.valueOf(priority), pageable);
        } else if (technician != null) {
            entities = requestService.repository.findByAssignedTechnician(technician, pageable);
        } else {
            entities = requestService.repository.findAll(pageable);
        }
        Page<MaintenanceRequestResponse> responses = entities.map(mapper::toResponse);
        PagedResponse<MaintenanceRequestResponse> pageDto = new PagedResponse<>(
                responses.getContent(),
                responses.getNumber(),
                responses.getSize(),
                responses.getTotalElements(),
                responses.getTotalPages(),
                responses.isLast()
        );
        return ResponseEntity.ok(new ApiResponse<>(200, "Maintenance requests retrieved", pageDto));
    }
    @GetMapping("/{id}")
    @Operation(summary = "Get a maintenance request by its UUID")
    @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Request details")
    public ResponseEntity<ApiResponse<MaintenanceRequestResponse>> getRequest(@PathVariable UUID id) {
        MaintenanceRequestResponse resp = requestService.getById(id);
        return ResponseEntity.ok(new ApiResponse<>(200, "Maintenance request retrieved", resp));
    }

    @PatchMapping("/{id}")
    @Operation(summary = "Update mutable fields of a maintenance request")
    @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Request updated")
    public ResponseEntity<ApiResponse<MaintenanceRequestResponse>> updateRequest(
            @PathVariable UUID id,
            @Valid @RequestBody UpdateMaintenanceRequest dto) {
        MaintenanceRequestResponse resp = requestService.updateRequest(id, dto);
        return ResponseEntity.ok(new ApiResponse<>(200, "Maintenance request updated", resp));
    }

    @PostMapping("/{id}/complete")
    @Operation(summary = "Mark a maintenance request as completed and publish events")
    @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Request completed")
    public ResponseEntity<ApiResponse<MaintenanceRequestResponse>> completeRequest(
            @PathVariable UUID id,
            @Valid @RequestBody CompleteMaintenanceRequest dto) {
        MaintenanceRequestResponse resp = requestService.completeRequest(id, dto);
        return ResponseEntity.ok(new ApiResponse<>(200, "Maintenance request completed", resp));
    }

    @PostMapping("/{id}/cancel")
    @Operation(summary = "Cancel a maintenance request")
    @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Request cancelled")
    public ResponseEntity<ApiResponse<MaintenanceRequestResponse>> cancelRequest(@PathVariable UUID id) {
        var request = requestService.repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Request not found"));
        request.setStatus(MaintenanceStatus.CANCELLED);
        requestService.repository.save(request);
        MaintenanceRequestResponse resp = mapper.toResponse(request);
        return ResponseEntity.ok(new ApiResponse<>(200, "Maintenance request cancelled", resp));
    }

    @GetMapping("/open-by-room/{roomId}")
    @Operation(summary = "Get all open (non‑COMPLETED/CANCELLED) requests for a given room")
    @io.swagger.v3.oas.annotations.responses.ApiResponse(responseCode = "200", description = "Open requests for room")
    public ResponseEntity<ApiResponse<PagedResponse<MaintenanceRequestResponse>>> getOpenByRoom(
            @PathVariable String roomId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        Pageable pageable = PageRequest.of(page, size);
        var openStatuses = java.util.List.of(
                MaintenanceStatus.PENDING,
                MaintenanceStatus.ASSIGNED,
                MaintenanceStatus.IN_PROGRESS,
                MaintenanceStatus.WAITING_FOR_PARTS
        );
        Page<MaintenanceRequest> entities = requestService.repository.findByRoomIdAndStatusIn(roomId, openStatuses, pageable);
}
}
