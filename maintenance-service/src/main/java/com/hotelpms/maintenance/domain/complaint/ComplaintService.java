package com.hotelpms.maintenance.domain.complaint;

import com.hotelpms.maintenance.domain.complaint.dto.*;
import com.hotelpms.maintenance.domain.complaint.mapper.ComplaintMapper;
import com.hotelpms.maintenance.domain.request.MaintenanceRequestService;
import com.hotelpms.maintenance.domain.request.dto.CreateMaintenanceRequest;
import com.hotelpms.maintenance.shared.enums.ComplaintStatus;
import com.hotelpms.maintenance.shared.enums.Priority;
import com.hotelpms.maintenance.shared.exception.ResourceNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ComplaintService {
    
    private final ComplaintRepository repository;
    private final ComplaintMapper mapper;
    private final MaintenanceRequestService maintenanceRequestService;

    @Transactional
    public ComplaintResponse createComplaint(CreateComplaintRequest request) {
        Complaint complaint = Complaint.builder()
                .guestName(request.getGuestName())
                .roomId(request.getRoomId())
                .bookingRef(request.getBookingRef())
                .category(request.getCategory())
                .description(request.getDescription())
                .urgency(request.getUrgency())
                .recordedBy(request.getRecordedBy())
                .photoUrls(request.getPhotoUrls())
                .complaintDate(Instant.now())
                .status(ComplaintStatus.OPEN)
                .build();

        Complaint saved = repository.save(complaint);
        return mapper.toResponse(saved);
    }

    public Page<Complaint> findAll(Pageable pageable) {
        return repository.findAll(pageable);
    }

    public Page<Complaint> findByRoomId(String roomId, Pageable pageable) {
        return repository.findByRoomId(roomId, pageable);
    }

    public Page<Complaint> findByBookingRef(String bookingRef, Pageable pageable) {
        return repository.findByBookingRef(bookingRef, pageable);
    }

    public Page<Complaint> findByUrgency(Priority urgency, Pageable pageable) {
        return repository.findByUrgency(urgency, pageable);
    }

    public Page<Complaint> findByStatus(ComplaintStatus status, Pageable pageable) {
        return repository.findByStatus(status, pageable);
    }

    public ComplaintResponse getById(UUID id) {
        return repository.findById(id)
                .map(mapper::toResponse)
                .orElseThrow(() -> new ResourceNotFoundException("Complaint not found"));
    }

    @Transactional
    public ComplaintResponse updateComplaint(UUID id, UpdateComplaintRequest request) {
        Complaint complaint = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Complaint not found"));
        
        if (request.getStatus() != null) complaint.setStatus(request.getStatus());
        if (request.getResolutionNotes() != null) complaint.setResolutionNotes(request.getResolutionNotes());
        
        return mapper.toResponse(repository.save(complaint));
    }

    @Transactional
    public void forwardComplaint(UUID id, String reportedBy) {
        Complaint complaint = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Complaint not found"));

        CreateMaintenanceRequest maintenanceDto = new CreateMaintenanceRequest();
        maintenanceDto.setRoomId(complaint.getRoomId());
        maintenanceDto.setIssueType(complaint.getCategory().name());
        maintenanceDto.setDescription("Forwarded from Complaint: " + complaint.getDescription());
        maintenanceDto.setPriority(complaint.getUrgency());
        maintenanceDto.setReportedBy(reportedBy);
        // Note: You might want to extend the DTO to include complaintId to link them in the DB

        var maintenanceResponse = maintenanceRequestService.createRequest(maintenanceDto);
        complaint.setMaintenanceRequestId(maintenanceResponse.getId());
        complaint.setStatus(ComplaintStatus.FORWARDED_TO_MAINTENANCE);
        repository.save(complaint);
    }
}