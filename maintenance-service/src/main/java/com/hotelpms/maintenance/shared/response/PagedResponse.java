package com.hotelpms.maintenance.shared.response;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Wrapper for paginated responses.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Paginated response containing data and pagination metadata")
public class PagedResponse<T> {
    @Schema(description = "Content list for the current page")
    private List<T> content;

    @Schema(description = "Zero‑based page index", example = "0")
    private int page;

    @Schema(description = "Size of the page (number of elements)", example = "20")
    private int size;

    @Schema(description = "Total number of elements across all pages", example = "124")
    private long totalElements;

    @Schema(description = "Total number of pages", example = "7")
    private int totalPages;

    @Schema(description = "Whether this is the last page", example = "false")
    private boolean last;
}