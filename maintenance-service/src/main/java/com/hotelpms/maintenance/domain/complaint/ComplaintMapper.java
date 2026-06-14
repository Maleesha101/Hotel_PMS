package com.hotelpms.maintenance.domain.complaint.mapper;

import com.hotelpms.maintenance.domain.complaint.Complaint;
import com.hotelpms.maintenance.domain.complaint.dto.ComplaintResponse;
import org.mapstruct.Mapper;
import org.mapstruct.ReportingPolicy;

@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface ComplaintMapper {
    ComplaintResponse toResponse(Complaint entity);
}