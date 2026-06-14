package com.hotelpms.maintenance.domain.equipment;

import com.hotelpms.maintenance.shared.enums.EquipmentType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;

import java.sql.Date;
import java.util.List;
import java.util.UUID;

/**
 * Spring Data JPA repository for {@link Equipment} entities.
 */
@Repository
public interface EquipmentRepository extends JpaRepository<Equipment, UUID>, JpaSpecificationExecutor<Equipment> {
    Page<Equipment> findByEquipmentType(EquipmentType equipmentType, Pageable pageable);
    Page<Equipment> findByLocation(String location, Pageable pageable);
    Page<Equipment> findByStatus(String status, Pageable pageable);
    List<Equipment> findByNextServiceDateLessThanEqual(Date date);
}
