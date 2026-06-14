package com.hotelpms.maintenance.domain.request.mapper;

import com.hotelpms.maintenance.domain.request.MaintenanceRequest;
import com.hotelpms.maintenance.domain.request.dto.MaintenanceRequestResponse;
import javax.annotation.processing.Generated;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2026-06-14T20:41:26+0530",
    comments = "version: 1.5.5.Final, compiler: javac, environment: Java 17.0.12 (Oracle Corporation)"
)
@Component
public class MaintenanceRequestMapperImpl implements MaintenanceRequestMapper {

    @Override
    public MaintenanceRequestResponse toResponse(MaintenanceRequest entity) {
        if ( entity == null ) {
            return null;
        }

        MaintenanceRequestResponse maintenanceRequestResponse = new MaintenanceRequestResponse();

        maintenanceRequestResponse.setId( entity.getId() );
        maintenanceRequestResponse.setRoomId( entity.getRoomId() );
        maintenanceRequestResponse.setDescription( entity.getDescription() );
        maintenanceRequestResponse.setPriority( entity.getPriority() );
        maintenanceRequestResponse.setStatus( entity.getStatus() );
        maintenanceRequestResponse.setAssignedTechnician( entity.getAssignedTechnician() );
        maintenanceRequestResponse.setCreatedAt( entity.getCreatedAt() );
        maintenanceRequestResponse.setUpdatedAt( entity.getUpdatedAt() );
        maintenanceRequestResponse.setCompletedAt( entity.getCompletedAt() );
        maintenanceRequestResponse.setCompletionNotes( entity.getCompletionNotes() );

        return maintenanceRequestResponse;
    }
}
