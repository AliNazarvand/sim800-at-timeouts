#include "sim800_at_timeouts/timeout_types.hpp"
#include <string_view>

// Self-contained: demonstrates the structural rules for
// source_same_as_representative / page_hint_same_as_representative.
int run_same_source_example() {
    using namespace sim800::timeouts;

    VersionEntry ve{};
    ve.version = "V1.10";
    ve.presence_status = PresenceStatus::NotMentioned;
    ve.extraction_status = ExtractionStatus::NotSpecified;
    ve.source_same_as_representative = true;
    ve.page_hint_same_as_representative = true;
    ve.source_document = std::string_view{};
    ve.source_section = std::string_view{};
    ve.page_hint = PAGE_UNSET;

    if (!ve.source_same_as_representative) return 1;
    if (!ve.page_hint_same_as_representative) return 2;
    if (!ve.source_document.empty()) return 3;
    if (!ve.source_section.empty()) return 4;
    if (ve.page_hint != PAGE_UNSET) return 5;
    return 0;
}