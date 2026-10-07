// ============================================================
// AUTO-GENERATED FILE — DO NOT EDIT MANUALLY
// Generated from: data/http.yaml
// Content hash (SHA-256 of entries section only): 01fc6c5cda9497ea43f124a12400769c557b7528db418db22f8f1000ab95951d
// Generator: scripts/generate_headers.py
// Database version: 1.0.0
// To regenerate: cmake --build . --target generate
// ============================================================

#pragma once
#include "timeout_types.hpp"
#include "database_version.hpp"
#include <array>
#include <cstddef>
#include <string_view>
#include <algorithm>

namespace sim800::timeouts::http {

inline constexpr std::array<CommandEntry, 3> HTTP_TIMEOUTS = {{
    {
        "AT+HTTPACTION",
        Category::Http,
        "HTTP action",
        {{
            { TimeoutKind::MaxTimeout, MS_UNSET, 60000u, MS_UNSET, MS_UNSET, MS_UNSET },
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        1,
        "SIM800 Series_AT Command Manual_V1.10.pdf",
        "Section AT+HTTPACTION",
        ExtractionStatus::ExtractedFromText,
        PresenceStatus::Present,
        "V1.10",
        {{ "V1.01", "V1.10", {}, {}, {}, {}, {}, {} }},
        2,
        {{}},
        0,
        {{
            {
                "V1.01",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section AT+HTTPACTION", 100u, "Confirmed identical to V1.10.", "V1.10" }
            },
            {
                "V1.12",
                ReviewStatus::ApprovedRemovedCommand,
                true,
                ReviewEvidence{ "Chapter 8", 130u, "Command removed; not present in V1.12 TOC.", "" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        112u,
        "Removed in V1.12; representative version is V1.10."
    },
    {
        "AT+HTTPINIT",
        Category::Http,
        "Initialize HTTP service",
        {{
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        0,
        "SIM800 Series_AT Command Manual_V1.10.pdf",
        "Section 11.2.1 AT+HTTPINIT",
        ExtractionStatus::NotSpecified,
        PresenceStatus::NotMentioned,
        "V1.10",
        {{ "V1.01", "V1.10", {}, {}, {}, {}, {}, {} }},
        2,
        {{}},
        0,
        {{
            {
                "V1.01",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Table 11.2.1 AT+HTTPINIT", 108u, "Confirmed identical to V1.10.", "V1.10" }
            },
            {
                "V1.12",
                ReviewStatus::ApprovedAbsentCommand,
                true,
                ReviewEvidence{ "Chapter 8", 130u, "Command not present in V1.12.", "" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        108u,
        ""
    },
    {
        "AT+HTTPREAD",
        Category::Http,
        "Read the HTTP server response",
        {{
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        0,
        "SIM800 Series_AT Command Manual_V1.10.pdf",
        "Section 11.2.6 AT+HTTPREAD",
        ExtractionStatus::NotSpecified,
        PresenceStatus::NotMentioned,
        "V1.10",
        {{ "V1.01", "V1.10", {}, {}, {}, {}, {}, {} }},
        2,
        {{}},
        0,
        {{
            {
                "V1.01",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Table 11.2.6 AT+HTTPREAD", 115u, "Confirmed identical to V1.10.", "V1.10" }
            },
            {
                "V1.12",
                ReviewStatus::ApprovedAbsentCommand,
                true,
                ReviewEvidence{ "Chapter 8", 130u, "Command not present in V1.12.", "" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        115u,
        "When cmd_type is 1, 85 seconds"
    }
}};

inline constexpr std::size_t HTTP_TIMEOUTS_COUNT = HTTP_TIMEOUTS.size();
static_assert(HTTP_TIMEOUTS_COUNT <= MAX_ENTRIES_PER_HEADER,
              "HTTP_TIMEOUTS entry count exceeds MAX_ENTRIES_PER_HEADER");

inline constexpr std::array<std::string_view, HTTP_TIMEOUTS_COUNT> HTTP_TIMEOUTS_COMMAND_INDEX = {{
    "AT+HTTPACTION",
    "AT+HTTPINIT",
    "AT+HTTPREAD"
}};

inline const CommandEntry* find_http_entry(std::string_view cmd) noexcept {
    auto it = std::lower_bound(HTTP_TIMEOUTS_COMMAND_INDEX.begin(), HTTP_TIMEOUTS_COMMAND_INDEX.end(), cmd);
    if (it == HTTP_TIMEOUTS_COMMAND_INDEX.end() || *it != cmd) return nullptr;
    return &HTTP_TIMEOUTS[static_cast<std::size_t>(it - HTTP_TIMEOUTS_COMMAND_INDEX.begin())];
}

} // namespace sim800::timeouts::http
