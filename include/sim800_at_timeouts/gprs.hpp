// ============================================================
// AUTO-GENERATED FILE — DO NOT EDIT MANUALLY
// Generated from: data/gprs.yaml
// Content hash (SHA-256 of entries section only): 66059f372c52ebbfdc2e78e26d90cc0854450c0d1022a8ece5831867adcc5ea4
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

namespace sim800::timeouts::gprs {

inline constexpr std::array<CommandEntry, 1> GPRS_TIMEOUTS = {{
    {
        "AT+CGDCONT",
        Category::Gprs,
        "Define PDP context",
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
        "SIM800 Series_AT Command Manual_V1.12.pdf",
        "Section 7.2.2 AT+CGDCONT",
        ExtractionStatus::NotSpecified,
        PresenceStatus::NotMentioned,
        "V1.12",
        {{ "V1.01", "V1.10", "V1.12", {}, {}, {}, {}, {} }},
        3,
        {{}},
        0,
        {{
            {
                "V1.01",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 7.2.2 AT+CGDCONT", 212u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 7.2.2 AT+CGDCONT", 212u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        212u,
        ""
    }
}};

inline constexpr std::size_t GPRS_TIMEOUTS_COUNT = GPRS_TIMEOUTS.size();
static_assert(GPRS_TIMEOUTS_COUNT <= MAX_ENTRIES_PER_HEADER,
              "GPRS_TIMEOUTS entry count exceeds MAX_ENTRIES_PER_HEADER");

inline constexpr std::array<std::string_view, GPRS_TIMEOUTS_COUNT> GPRS_TIMEOUTS_COMMAND_INDEX = {{
    "AT+CGDCONT"
}};

inline const CommandEntry* find_gprs_entry(std::string_view cmd) noexcept {
    auto it = std::lower_bound(GPRS_TIMEOUTS_COMMAND_INDEX.begin(), GPRS_TIMEOUTS_COMMAND_INDEX.end(), cmd);
    if (it == GPRS_TIMEOUTS_COMMAND_INDEX.end() || *it != cmd) return nullptr;
    return &GPRS_TIMEOUTS[static_cast<std::size_t>(it - GPRS_TIMEOUTS_COMMAND_INDEX.begin())];
}

} // namespace sim800::timeouts::gprs
