package com.hotelpms.maintenance.domain.request;

import com.hotelpms.maintenance.domain.request.dto.*;
import com.hotelpms.maintenance.domain.request.mapper.MaintenanceRequestMapper;
import com.hotelpms.maintenance.shared.enums.MaintenanceStatus;
import com.hotelpms.maintenance.shared.enums.Priority;
import com.hotelpms.maintenance.shared.exception.ResourceNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class MaintenanceRequestService {

    private final MaintenanceRequestRepository repository;
    private final MaintenanceRequestMapper mapper;

    @Transactional
    public MaintenanceRequestResponse createRequest(CreateMaintenanceRequest dto) {
        MaintenanceRequest request = MaintenanceRequest.builder()
                .roomId(dto.getRoomId())
                .locationNotes(dto.getLocationNotes())
                .issueType(dto.getIssueType())
                .description(dto.getDescription())
                .priority(dto.getPriority())
                .reportedBy(dto.getReportedBy())
                .photoUrls(dto.getPhotoUrls())
                .status(MaintenanceStatus.PENDING)
                .reportedDate(Instant.now())
                .isGuestChargeable(false)
                .build();

        MaintenanceRequest saved = repository.save(request);
        return mapper.toResponse(saved);
    }

    @Transactional(readOnly = true)
    public MaintenanceRequestResponse getById(UUID id) {
        return repository.findById(id)
                .map(mapper::toResponse)
                .orElseThrow(() -> new ResourceNotFoundException("Maintenance request not found"));
    }

    @Transactional(readOnly = true)
    public Page<MaintenanceRequestResponse> findByStatus(MaintenanceStatus status, Pageable pageable) {
        return repository.findByStatus(status, pageable).map(mapper::toResponse);
    }

    @Transactional(readOnly = true)
    public Page<MaintenanceRequestResponse> findByRoomId(String roomId, Pageable pageable) {
        return repository.findByRoomId(roomId, pageable).map(mapper::toResponse);
    }

    @Transactional(readOnly = true)
    public Page<MaintenanceRequestResponse> findByPriority(Priority priority, Pageable pageable) {
        return repository.findByPriority(priority, pageable).map(mapper::toResponse);
    }

    @Transactional(readOnly = true)
    public Page<MaintenanceRequestResponse> findByAssignedTechnician(String technician, Pageable pageable) {
        return repository.findByAssignedTechnician(technician, pageable).map(mapper::toResponse);
    }

    @Transactional(readOnly = true)
    public Page<MaintenanceRequestResponse> findAll(Pageable pageable) {
        return repository.findAll(pageable).map(mapper::toResponse);
    }

    @Transactional(readOnly = true)
    public Page<MaintenanceRequestResponse> findByRoomIdAndStatusIn(String roomId, List<MaintenanceStatus> statuses, Pageable pageable) {
        return repository.findByRoomIdAndStatusIn(roomId, statuses, pageable).map(mapper::toResponse);
    }

    @Transactional
    public MaintenanceRequestResponse updateRequest(UUID id, UpdateMaintenanceRequest dto) {
        MaintenanceRequest request = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Request not found"));
        
        if (dto.getStatus() != null) request.setStatus(dto.getStatus());
        if (dto.getPriority() != null) request.setPriority(dto.getPriority());
        if (dto.getAssignedTechnician() != null) request.setAssignedTechnician(dto.getAssignedTechnician());
        
        return mapper.toResponse(repository.save(request));
    }

    @Transactional
    public MaintenanceRequestResponse completeRequest(UUID id, CompleteMaintenanceRequest dto) {
        MaintenanceRequest request = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Request not found"));
        
        request.setStatus(MaintenanceStatus.COMPLETED);
        request.setCompletionNotes(dto.getCompletionNotes());
        request.setCompletedAt(Instant.now());
        
        return mapper.toResponse(repository.save(request));
    }

    @Transactional
    public MaintenanceRequestResponse cancelRequest(UUID id) {
        MaintenanceRequest request = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Request not found"));

        request.setStatus(MaintenanceStatus.CANCELLED);
        return mapper.toResponse(repository.save(request));
    }
}