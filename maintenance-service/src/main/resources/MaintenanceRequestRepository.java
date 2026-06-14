package com.hotelpms.maintenance.domain.request;

import com.hotelpms.maintenance.shared.enums.MaintenanceStatus;
import com.hotelpms.maintenance.shared.enums.Priority;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

/**
 * Spring Data JPA repository for {@link MaintenanceRequest} entities.
 */
@Repository
public interface MaintenanceRequestRepository extends JpaRepository<MaintenanceRequest, UUID> {
    Page<MaintenanceRequest> findByRoomId(String roomId, Pageable pageable);
    Page<MaintenanceRequest> findByStatus(MaintenanceStatus status, Pageable pageable);
    Page<MaintenanceRequest> findByPriority(Priority priority, Pageable pageable);
    Page<MaintenanceRequest> findByAssignedTechnician(String technician, Pageable pageable);
    List<MaintenanceRequest> findByRoomIdAndStatusIn(String roomId, List<MaintenanceStatus> statuses);
    Page<MaintenanceRequest> findByRoomIdAndStatusIn(String roomId, List<MaintenanceStatus> statuses, Pageable pageable);
}