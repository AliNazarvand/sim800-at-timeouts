// ============================================================
// AUTO-GENERATED FILE — DO NOT EDIT MANUALLY
// Generated from: data/at_3gpp.yaml
// Content hash (SHA-256 of entries section only): 05af2a8f4d415b671af6f11e9d4e3545e95d8e583c174bab0a9d92e7f811d0a3
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

namespace sim800::timeouts::at_3gpp {

inline constexpr std::array<CommandEntry, 11> AT_3GPP_TIMEOUTS = {{
    {
        "AT+CGACT",
        Category::At3gpp27007,
        "PDP context activate or deactivate",
        {{
            { TimeoutKind::MaxResponseTime, MS_UNSET, 150000u, MS_UNSET, MS_UNSET, MS_UNSET },
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
        "Section 7.2.5 AT+CGACT",
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
                ReviewEvidence{ "Page 175", 175u, "Auto-verified from PDF; MRT matches representative.", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 7.2.5 AT+CGACT", 213u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        213u,
        ""
    },
    {
        "AT+CGATT",
        Category::At3gpp27007,
        "Attach or detach from GPRS service",
        {{
            { TimeoutKind::MaxResponseTime, MS_UNSET, 75000u, MS_UNSET, MS_UNSET, MS_UNSET },
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
        "Section 7.2.1 AT+CGATT",
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
                ReviewEvidence{ "Section 7.2.1 AT+CGATT", 210u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Page 211", 211u, "Auto-verified from PDF; MRT matches representative.", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        210u,
        "70 seconds max response time"
    },
    {
        "AT+CGREG",
        Category::At3gpp27007,
        "Network registration status for GPRS",
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
        "Section 7.2.10 AT+CGREG",
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
                ReviewEvidence{ "Section 7.2.10 AT+CGREG", 218u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 7.2.10 AT+CGREG", 218u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        218u,
        ""
    },
    {
        "AT+CGSN",
        Category::At3gpp27007,
        "Request International Mobile Equipment Identity (IMEI)",
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
        "Chapter 3",
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
                ReviewEvidence{ "Chapter 3", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Chapter 3", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
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
        "Command present in manual; timeout not mentioned in PDF."
    },
    {
        "AT+CMEE",
        Category::At3gpp27007,
        "Report mobile equipment error",
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
        "Chapter 3",
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
                ReviewEvidence{ "Chapter 3", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Chapter 3", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
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
        "Command present in manual; timeout not mentioned in PDF."
    },
    {
        "AT+CNMI",
        Category::At3gpp27005,
        "New message indication to TE",
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
        "Chapter 4",
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
                ReviewEvidence{ "Chapter 4", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Chapter 4", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
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
        "Command present in manual; timeout not mentioned in PDF."
    },
    {
        "AT+COPS",
        Category::At3gpp27007,
        "Operator selection",
        {{
            { TimeoutKind::MaxResponseTime, 45000u, 120000u, MS_UNSET, MS_UNSET, MS_UNSET },
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
        "Section 3.2.22 AT+COPS",
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
                ReviewEvidence{ "Section 3.2.22 AT+COPS", 78u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 3.2.22 AT+COPS", 78u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        78u,
        "Test command: 45s; Write command: 120s."
    },
    {
        "AT+CPIN",
        Category::At3gpp27007,
        "Enter PIN",
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
        "Section 3.2.1 AT+CPIN",
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
                ReviewEvidence{ "Section 3.2.1 AT+CPIN", 72u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Table 3.2.1 AT+CPIN", 72u, "Confirmed identical max response time values.", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        72u,
        "3s for string present; 30s for complete phonebook read."
    },
    {
        "AT+CPMS",
        Category::At3gpp27005,
        "Preferred message storage",
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
        "Chapter 4",
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
                ReviewEvidence{ "Chapter 4", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Chapter 4", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
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
        "Command present in manual; timeout not mentioned in PDF."
    },
    {
        "AT+CREG",
        Category::At3gpp27007,
        "Network registration status",
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
        "Section 3.2.32 AT+CREG",
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
                ReviewEvidence{ "Section 3.2.32 AT+CREG", 82u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 3.2.32 AT+CREG", 82u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        82u,
        ""
    },
    {
        "AT+CSQ",
        Category::At3gpp27007,
        "Signal quality report",
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
        "Section 3.2.35 AT+CSQ",
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
                ReviewEvidence{ "Section 3.2.35 AT+CSQ", 88u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 3.2.35 AT+CSQ", 88u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        88u,
        ""
    }
}};

inline constexpr std::size_t AT_3GPP_TIMEOUTS_COUNT = AT_3GPP_TIMEOUTS.size();
static_assert(AT_3GPP_TIMEOUTS_COUNT <= MAX_ENTRIES_PER_HEADER,
              "AT_3GPP_TIMEOUTS entry count exceeds MAX_ENTRIES_PER_HEADER");

inline constexpr std::array<std::string_view, AT_3GPP_TIMEOUTS_COUNT> AT_3GPP_TIMEOUTS_COMMAND_INDEX = {{
    "AT+CGACT",
    "AT+CGATT",
    "AT+CGREG",
    "AT+CGSN",
    "AT+CMEE",
    "AT+CNMI",
    "AT+COPS",
    "AT+CPIN",
    "AT+CPMS",
    "AT+CREG",
    "AT+CSQ"
}};

inline const CommandEntry* find_at_3gpp_entry(std::string_view cmd) noexcept {
    auto it = std::lower_bound(AT_3GPP_TIMEOUTS_COMMAND_INDEX.begin(), AT_3GPP_TIMEOUTS_COMMAND_INDEX.end(), cmd);
    if (it == AT_3GPP_TIMEOUTS_COMMAND_INDEX.end() || *it != cmd) return nullptr;
    return &AT_3GPP_TIMEOUTS[static_cast<std::size_t>(it - AT_3GPP_TIMEOUTS_COMMAND_INDEX.begin())];
}

} // namespace sim800::timeouts::at_3gpp
