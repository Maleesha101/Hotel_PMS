package com.hotelpms.maintenance.domain.request.mapper;

import com.hotelpms.maintenance.domain.request.MaintenanceRequest;
import com.hotelpms.maintenance.domain.request.dto.MaintenanceRequestResponse;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface MaintenanceRequestMapper {
    MaintenanceRequestResponse toResponse(MaintenanceRequest entity);
}