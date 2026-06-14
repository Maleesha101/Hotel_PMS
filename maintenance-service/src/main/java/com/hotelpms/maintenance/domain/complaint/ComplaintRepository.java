package com.hotelpms.maintenance.domain.complaint;

import com.hotelpms.maintenance.shared.enums.ComplaintStatus;
import com.hotelpms.maintenance.shared.enums.Priority;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;

import java.util.UUID;

/**
 * Spring Data JPA repository for {@link Complaint} entities.
 */
@Repository
public interface ComplaintRepository extends JpaRepository<Complaint, UUID>, JpaSpecificationExecutor<Complaint> {
    Page<Complaint> findByRoomId(String roomId, Pageable pageable);
    Page<Complaint> findByStatus(ComplaintStatus status, Pageable pageable);
    Page<Complaint> findByBookingRef(String bookingRef, Pageable pageable);
    Page<Complaint> findByUrgency(Priority urgency, Pageable pageable);
    // Additional filter combinations can be added as needed
}
