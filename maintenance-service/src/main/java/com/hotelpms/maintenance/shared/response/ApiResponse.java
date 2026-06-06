package com.hotelpms.maintenance.shared.response;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Standard API response wrapper.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Standard response object wrapping payload and metadata")
public class ApiResponse<T> {
    @Schema(description = "HTTP status code", example = "200")
    private int status;

    @Schema(description = "Message describing the result", example = "Success")
    private String message;

    @Schema(description = "Payload data (may be null)")
    private T data;
}