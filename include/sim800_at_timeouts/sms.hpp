// ============================================================
// AUTO-GENERATED FILE — DO NOT EDIT MANUALLY
// Generated from: data/sms.yaml
// Content hash (SHA-256 of entries section only): f97ace9b3f33e8ddd1e44dc8519d70082189b1b1c939609969f75e0d0b5ae321
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

namespace sim800::timeouts::sms {

inline constexpr std::array<CommandEntry, 5> SMS_TIMEOUTS = {{
    {
        "AT+CMGD",
        Category::Sms,
        "Delete SMS message",
        {{
            { TimeoutKind::MaxResponseTime, MS_UNSET, 5000u, MS_UNSET, MS_UNSET, MS_UNSET },
            { TimeoutKind::MaxTimeout, 5000u, 25000u, MS_UNSET, MS_UNSET, MS_UNSET },
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        2,
        "SIM800 Series_AT Command Manual_V1.12.pdf",
        "Section 4.2.1 AT+CMGD",
        ExtractionStatus::ExtractedFromTable,
        PresenceStatus::Present,
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
                ReviewEvidence{ "Table 4.2.1 AT+CMGD", 44u, "Confirmed identical to V1.12.", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Table 4.2.1 AT+CMGD", 44u, "Confirmed identical to V1.12.", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        44u,
        "delete 1 msg: 5s; delete 50/150 msgs: 25s"
    },
    {
        "AT+CMGF",
        Category::Sms,
        "Set SMS message format",
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
        "Section 4.2.2 AT+CMGF",
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
                ReviewEvidence{ "Section AT+CMGF", 46u, "Confirmed identical to V1.12.", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section AT+CMGF", 46u, "Confirmed identical to V1.12.", "V1.12" }
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
    },
    {
        "AT+CMGL",
        Category::Sms,
        "List SMS messages from preferred store",
        {{
            { TimeoutKind::MaxResponseTime, MS_UNSET, 20000u, MS_UNSET, MS_UNSET, MS_UNSET },
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        1,
        "SIM800 Series_AT Command Manual_V1.12.pdf",
        "Section 4.2.3 AT+CMGL",
        ExtractionStatus::ExtractedFromTable,
        PresenceStatus::Present,
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
                ReviewEvidence{ "Page 106", 106u, "Phase-12: version_specific removed earlier; timeouts confirmed identical to representative. (was: Auto-generated: MRT differs (20000 ms vs 5000 ms).)", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Page 117", 117u, "Phase-12: version_specific removed earlier; timeouts confirmed identical to representative. (was: Auto-generated: MRT differs (20000 ms vs 5000 ms).)", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        47u,
        ""
    },
    {
        "AT+CMGR",
        Category::Sms,
        "Read SMS message",
        {{
            { TimeoutKind::MaxResponseTime, MS_UNSET, 5000u, MS_UNSET, MS_UNSET, MS_UNSET },
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        1,
        "SIM800 Series_AT Command Manual_V1.12.pdf",
        "Section 4.2.4 AT+CMGR",
        ExtractionStatus::ExtractedFromTable,
        PresenceStatus::Present,
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
                ReviewEvidence{ "Section 4.2.4 AT+CMGR", 49u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Page 120", 120u, "Auto-verified from PDF; MRT matches representative.", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        49u,
        ""
    },
    {
        "AT+CMGS",
        Category::Sms,
        "Send message",
        {{
            { TimeoutKind::PromptTimeout, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET },
            { TimeoutKind::SendTimeout, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET },
            { TimeoutKind::MaxResponseTime, MS_UNSET, 60000u, MS_UNSET, MS_UNSET, MS_UNSET },
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        3,
        "SIM800 Series_AT Command Manual_V1.12.pdf",
        "Section 4.2.5 AT+CMGS",
        ExtractionStatus::ExtractedFromTable,
        PresenceStatus::Present,
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
                ReviewEvidence{ "Section AT+CMGS", 45u, "Confirmed identical to V1.12.", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section AT+CMGS", 45u, "Confirmed identical to V1.12.", "V1.12" }
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
        "DR-6: prompt_timeout (>) + send_timeout (Ctrl+Z) + max_response_time 60s."
    }
}};

inline constexpr std::size_t SMS_TIMEOUTS_COUNT = SMS_TIMEOUTS.size();
static_assert(SMS_TIMEOUTS_COUNT <= MAX_ENTRIES_PER_HEADER,
              "SMS_TIMEOUTS entry count exceeds MAX_ENTRIES_PER_HEADER");

inline constexpr std::array<std::string_view, SMS_TIMEOUTS_COUNT> SMS_TIMEOUTS_COMMAND_INDEX = {{
    "AT+CMGD",
    "AT+CMGF",
    "AT+CMGL",
    "AT+CMGR",
    "AT+CMGS"
}};

inline const CommandEntry* find_sms_entry(std::string_view cmd) noexcept {
    auto it = std::lower_bound(SMS_TIMEOUTS_COMMAND_INDEX.begin(), SMS_TIMEOUTS_COMMAND_INDEX.end(), cmd);
    if (it == SMS_TIMEOUTS_COMMAND_INDEX.end() || *it != cmd) return nullptr;
    return &SMS_TIMEOUTS[static_cast<std::size_t>(it - SMS_TIMEOUTS_COMMAND_INDEX.begin())];
}

} // namespace sim800::timeouts::sms
