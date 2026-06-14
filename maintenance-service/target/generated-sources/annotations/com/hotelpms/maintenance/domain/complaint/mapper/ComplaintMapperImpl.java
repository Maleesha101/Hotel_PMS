package com.hotelpms.maintenance.domain.complaint.mapper;

import com.hotelpms.maintenance.domain.complaint.Complaint;
import com.hotelpms.maintenance.domain.complaint.dto.ComplaintResponse;
import java.util.ArrayList;
import java.util.List;
import javax.annotation.processing.Generated;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2026-06-14T20:41:26+0530",
    comments = "version: 1.5.5.Final, compiler: javac, environment: Java 17.0.12 (Oracle Corporation)"
)
@Component
public class ComplaintMapperImpl implements ComplaintMapper {

    @Override
    public ComplaintResponse toResponse(Complaint entity) {
        if ( entity == null ) {
            return null;
        }

        ComplaintResponse complaintResponse = new ComplaintResponse();

        complaintResponse.setId( entity.getId() );
        complaintResponse.setGuestName( entity.getGuestName() );
        complaintResponse.setRoomId( entity.getRoomId() );
        complaintResponse.setBookingRef( entity.getBookingRef() );
        complaintResponse.setComplaintDate( entity.getComplaintDate() );
        complaintResponse.setCategory( entity.getCategory() );
        complaintResponse.setDescription( entity.getDescription() );
        complaintResponse.setUrgency( entity.getUrgency() );
        complaintResponse.setStatus( entity.getStatus() );
        complaintResponse.setRecordedBy( entity.getRecordedBy() );
        complaintResponse.setResolutionNotes( entity.getResolutionNotes() );
        List<String> list = entity.getPhotoUrls();
        if ( list != null ) {
            complaintResponse.setPhotoUrls( new ArrayList<String>( list ) );
        }
        complaintResponse.setCreatedAt( entity.getCreatedAt() );
        complaintResponse.setUpdatedAt( entity.getUpdatedAt() );

        return complaintResponse;
    }
}
