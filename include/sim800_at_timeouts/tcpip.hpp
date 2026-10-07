// ============================================================
// AUTO-GENERATED FILE — DO NOT EDIT MANUALLY
// Generated from: data/tcpip.yaml
// Content hash (SHA-256 of entries section only): 9e061aeb738ff3a7cc9cc6e5565407d725cf1496527df0aa26da2e0277d42fd1
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

namespace sim800::timeouts::tcpip {

inline constexpr std::array<CommandEntry, 9> TCPIP_TIMEOUTS = {{
    {
        "AT+CIFSR",
        Category::Tcpip,
        "Get local IP address",
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
        "Section 8.2.11 AT+CIFSR",
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
                ReviewEvidence{ "Section 8.2.11 AT+CIFSR", 231u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 8.2.11 AT+CIFSR", 231u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        231u,
        ""
    },
    {
        "AT+CIICR",
        Category::Tcpip,
        "Bring up wireless connection with GPRS or CSD",
        {{
            { TimeoutKind::MaxResponseTime, MS_UNSET, 85000u, MS_UNSET, MS_UNSET, MS_UNSET },
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
        "Section 8.2.10 AT+CIICR",
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
                ReviewEvidence{ "Section 8.2.10 AT+CIICR", 229u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Table 8.2.10 AT+CIICR", 229u, "Confirmed identical to V1.12.", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        229u,
        ""
    },
    {
        "AT+CIPCLOSE",
        Category::Tcpip,
        "Close TCP or UDP connection",
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
        "Section 8.2.6 AT+CIPCLOSE",
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
                ReviewEvidence{ "Section 8.2.6 AT+CIPCLOSE", 226u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 8.2.6 AT+CIPCLOSE", 226u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        226u,
        "multi-IP state: 75s; single IP state, IP INITIAL: 160s"
    },
    {
        "AT+CIPMUX",
        Category::Tcpip,
        "Start up multi-IP connection",
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
        "Chapter 8",
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
                ReviewEvidence{ "Chapter 8", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Chapter 8", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
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
        "AT+CIPSEND",
        Category::Tcpip,
        "Send data through TCP or UDP connection",
        {{
            { TimeoutKind::PromptTimeout, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET },
            { TimeoutKind::SendTimeout, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET },
            { TimeoutKind::UrcReportTimeout, MS_UNSET, 660000u, MS_UNSET, MS_UNSET, MS_UNSET },
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        3,
        "SIM800 Series_AT Command Manual_V1.12.pdf",
        "Section 8.2.3 AT+CIPSEND",
        ExtractionStatus::ExtractedFromText,
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
                ReviewEvidence{ "Section 8.2.3 AT+CIPSEND", 223u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 8.2.3 AT+CIPSEND", 223u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        223u,
        "URC CLOSE reported after 660 s when server not responding."
    },
    {
        "AT+CIPSHUT",
        Category::Tcpip,
        "Deactivate GPRS PDP context",
        {{
            { TimeoutKind::MaxResponseTime, MS_UNSET, 65000u, MS_UNSET, MS_UNSET, MS_UNSET },
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
        "Section 8.2.7 AT+CIPSHUT",
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
                ReviewEvidence{ "Section 8.2.7 AT+CIPSHUT", 227u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Page 230", 230u, "Auto-verified from PDF; MRT matches representative.", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        227u,
        ""
    },
    {
        "AT+CIPSTART",
        Category::Tcpip,
        "Start up TCP or UDP connection",
        {{
            { TimeoutKind::MaxTimeout, 75000u, 160000u, MS_UNSET, MS_UNSET, MS_UNSET },
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
        "Section 8.2.2 AT+CIPSTART",
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
                ReviewEvidence{ "Section 8.2.2 AT+CIPSTART", 221u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 8.2.2 AT+CIPSTART", 221u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        221u,
        "multi-IP state: 75s; single IP state, IP INITIAL: 160s"
    },
    {
        "AT+CIPSTATUS",
        Category::Tcpip,
        "Query current connection status",
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
        "Chapter 8",
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
                ReviewEvidence{ "Chapter 8", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Chapter 8", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
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
        "AT+CSTT",
        Category::Tcpip,
        "Start task and set APN, user name, password",
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
        "Chapter 8",
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
                ReviewEvidence{ "Chapter 8", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Chapter 8", 1u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
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
    }
}};

inline constexpr std::size_t TCPIP_TIMEOUTS_COUNT = TCPIP_TIMEOUTS.size();
static_assert(TCPIP_TIMEOUTS_COUNT <= MAX_ENTRIES_PER_HEADER,
              "TCPIP_TIMEOUTS entry count exceeds MAX_ENTRIES_PER_HEADER");

inline constexpr std::array<std::string_view, TCPIP_TIMEOUTS_COUNT> TCPIP_TIMEOUTS_COMMAND_INDEX = {{
    "AT+CIFSR",
    "AT+CIICR",
    "AT+CIPCLOSE",
    "AT+CIPMUX",
    "AT+CIPSEND",
    "AT+CIPSHUT",
    "AT+CIPSTART",
    "AT+CIPSTATUS",
    "AT+CSTT"
}};

inline const CommandEntry* find_tcpip_entry(std::string_view cmd) noexcept {
    auto it = std::lower_bound(TCPIP_TIMEOUTS_COMMAND_INDEX.begin(), TCPIP_TIMEOUTS_COMMAND_INDEX.end(), cmd);
    if (it == TCPIP_TIMEOUTS_COMMAND_INDEX.end() || *it != cmd) return nullptr;
    return &TCPIP_TIMEOUTS[static_cast<std::size_t>(it - TCPIP_TIMEOUTS_COMMAND_INDEX.begin())];
}

} // namespace sim800::timeouts::tcpip
