package com.hotelpms.maintenance.domain.equipment;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

/**
 * Repository for {@link EquipmentServiceHistory} entities.
 */
@Repository
public interface EquipmentServiceHistoryRepository extends JpaRepository<EquipmentServiceHistory, UUID> {
    Page<EquipmentServiceHistory> findByEquipmentId(UUID equipmentId, Pageable pageable);
    List<EquipmentServiceHistory> findByEquipmentIdOrderByServiceDateDesc(UUID equipmentId);
}