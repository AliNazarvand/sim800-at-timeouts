// ============================================================
// AUTO-GENERATED FILE — DO NOT EDIT MANUALLY
// Generated from: data/at_basic.yaml
// Content hash (SHA-256 of entries section only): 41257ca8b2f7ae6142df7a6275da12ca1721bd6b01d9c6c34b691205ee34f121
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

namespace sim800::timeouts::at_basic {

inline constexpr std::array<CommandEntry, 1> AT_BASIC_TIMEOUTS = {{
    {
        "AT",
        Category::AtBasic,
        "Test command",
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
        "Chapter 2",
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
                ReviewEvidence{ "Chapter 2", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Chapter 2", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        PAGE_UNSET,
        ""
    }
}};

inline constexpr std::size_t AT_BASIC_TIMEOUTS_COUNT = AT_BASIC_TIMEOUTS.size();
static_assert(AT_BASIC_TIMEOUTS_COUNT <= MAX_ENTRIES_PER_HEADER,
              "AT_BASIC_TIMEOUTS entry count exceeds MAX_ENTRIES_PER_HEADER");

inline constexpr std::array<std::string_view, AT_BASIC_TIMEOUTS_COUNT> AT_BASIC_TIMEOUTS_COMMAND_INDEX = {{
    "AT"
}};

inline const CommandEntry* find_at_basic_entry(std::string_view cmd) noexcept {
    auto it = std::lower_bound(AT_BASIC_TIMEOUTS_COMMAND_INDEX.begin(), AT_BASIC_TIMEOUTS_COMMAND_INDEX.end(), cmd);
    if (it == AT_BASIC_TIMEOUTS_COMMAND_INDEX.end() || *it != cmd) return nullptr;
    return &AT_BASIC_TIMEOUTS[static_cast<std::size_t>(it - AT_BASIC_TIMEOUTS_COMMAND_INDEX.begin())];
}

} // namespace sim800::timeouts::at_basic
