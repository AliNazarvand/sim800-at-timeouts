// ============================================================
// AUTO-GENERATED FILE — DO NOT EDIT MANUALLY
// Generated from: data/ftp.yaml
// Content hash (SHA-256 of entries section only): 7ed17f74a336524e50319126d1a4c4a78e2b609717dee89b9d44819eb928cc2a
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

namespace sim800::timeouts::ftp {

inline constexpr std::array<CommandEntry, 2> FTP_TIMEOUTS = {{
    {
        "AT+FTPGET",
        Category::Ftp,
        "Download file",
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
        "Section 12.2.14 AT+FTPGET",
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
                ReviewEvidence{ "Section 12.2.14 AT+FTPGET", 245u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Table 12.2.14 AT+FTPGET", 245u, "Confirmed identical to V1.12.", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        245u,
        ""
    },
    {
        "AT+FTPPUT",
        Category::Ftp,
        "Set upload file",
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
        "Section 12.2.15 AT+FTPPUT",
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
                ReviewEvidence{ "Section 12.2.15 AT+FTPPUT", 248u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Table 12.2.15 AT+FTPPUT", 248u, "Confirmed identical to V1.12.", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        248u,
        ""
    }
}};

inline constexpr std::size_t FTP_TIMEOUTS_COUNT = FTP_TIMEOUTS.size();
static_assert(FTP_TIMEOUTS_COUNT <= MAX_ENTRIES_PER_HEADER,
              "FTP_TIMEOUTS entry count exceeds MAX_ENTRIES_PER_HEADER");

inline constexpr std::array<std::string_view, FTP_TIMEOUTS_COUNT> FTP_TIMEOUTS_COMMAND_INDEX = {{
    "AT+FTPGET",
    "AT+FTPPUT"
}};

inline const CommandEntry* find_ftp_entry(std::string_view cmd) noexcept {
    auto it = std::lower_bound(FTP_TIMEOUTS_COMMAND_INDEX.begin(), FTP_TIMEOUTS_COMMAND_INDEX.end(), cmd);
    if (it == FTP_TIMEOUTS_COMMAND_INDEX.end() || *it != cmd) return nullptr;
    return &FTP_TIMEOUTS[static_cast<std::size_t>(it - FTP_TIMEOUTS_COMMAND_INDEX.begin())];
}

} // namespace sim800::timeouts::ftp
