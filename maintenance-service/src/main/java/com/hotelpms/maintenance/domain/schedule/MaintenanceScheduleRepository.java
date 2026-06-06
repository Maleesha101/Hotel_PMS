package com.hotelpms.maintenance.domain.schedule;

import com.hotelpms.maintenance.shared.enums.ScheduleStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Date;
import java.util.List;
import java.util.UUID;

/**
 * Repository for {@link MaintenanceSchedule} entities.
 */
@Repository
public interface MaintenanceScheduleRepository extends JpaRepository<MaintenanceSchedule, UUID> {
    Page<MaintenanceSchedule> findByEquipmentId(UUID equipmentId, Pageable pageable);
    List<MaintenanceSchedule> findByNextDueDateBeforeAndStatus(Date date, ScheduleStatus status);
    Page<MaintenanceSchedule> findByStatus(ScheduleStatus status, Pageable pageable);
}