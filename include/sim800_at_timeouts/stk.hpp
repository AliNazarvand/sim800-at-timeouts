// ============================================================
// AUTO-GENERATED FILE — DO NOT EDIT MANUALLY
// Generated from: data/stk.yaml
// Content hash (SHA-256 of entries section only): 89c8ddde4d1f4fc551ba178d6a86068ffe9ffae670ea6e981cdf25823d5a23ef
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

namespace sim800::timeouts::stk {

inline constexpr std::array<CommandEntry, 2> STK_TIMEOUTS = {{
    {
        "AT+STKCALL",
        Category::Stk,
        "STK call command",
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
        "Chapter 11",
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
                ReviewEvidence{ "Chapter 11", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Chapter 11", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
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
        "Command present in manual; timeout not yet extracted from PDF."
    },
    {
        "AT+STKMENU",
        Category::Stk,
        "STK menu",
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
        "Chapter 11",
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
                ReviewEvidence{ "Chapter 11", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Chapter 11", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
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
        "Command present in manual; timeout not yet extracted from PDF."
    }
}};

inline constexpr std::size_t STK_TIMEOUTS_COUNT = STK_TIMEOUTS.size();
static_assert(STK_TIMEOUTS_COUNT <= MAX_ENTRIES_PER_HEADER,
              "STK_TIMEOUTS entry count exceeds MAX_ENTRIES_PER_HEADER");

inline constexpr std::array<std::string_view, STK_TIMEOUTS_COUNT> STK_TIMEOUTS_COMMAND_INDEX = {{
    "AT+STKCALL",
    "AT+STKMENU"
}};

inline const CommandEntry* find_stk_entry(std::string_view cmd) noexcept {
    auto it = std::lower_bound(STK_TIMEOUTS_COMMAND_INDEX.begin(), STK_TIMEOUTS_COMMAND_INDEX.end(), cmd);
    if (it == STK_TIMEOUTS_COMMAND_INDEX.end() || *it != cmd) return nullptr;
    return &STK_TIMEOUTS[static_cast<std::size_t>(it - STK_TIMEOUTS_COMMAND_INDEX.begin())];
}

} // namespace sim800::timeouts::stk
