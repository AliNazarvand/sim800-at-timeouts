// ============================================================
// AUTO-GENERATED FILE — DO NOT EDIT MANUALLY
// Generated from: data/init.yaml
// Content hash (SHA-256 of entries section only): 9d8d6a7c206ac2fe2301c92975ca801033866423020d9e932bd28cfe29d2d6e0
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

namespace sim800::timeouts::init {

inline constexpr std::array<CommandEntry, 5> INIT_TIMEOUTS = {{
    {
        "BOOT_TIME_AFTER_PWRKEY",
        Category::Init,
        "Module boot time after PWRKEY release",
        {{
            { TimeoutKind::BootTime, MS_UNSET, 1600u, MS_UNSET, MS_UNSET, MS_UNSET },
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        1,
        "SIM800_Hardware Design_V1.09.pdf",
        "Section 4.2.1",
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
                ReviewEvidence{ "Section 4.2.1", 25u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 4.2.1", 25u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        25u,
        "Module successfully booted after about 1.6s"
    },
    {
        "PWRKEY_POWER_OFF",
        Category::Init,
        "Pull down PWRKEY to power off",
        {{
            { TimeoutKind::HardwareSettleTime, 1500u, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET },
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        1,
        "SIM800_Hardware Design_V1.09.pdf",
        "Section 4.2.2 Power off",
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
                ReviewEvidence{ "Section 4.2.2 Power off", 27u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 4.2.2 Power off", 27u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        27u,
        "At least 1.5 seconds"
    },
    {
        "PWRKEY_POWER_ON_SIM800",
        Category::Init,
        "Pull down PWRKEY to power on SIM800",
        {{
            { TimeoutKind::HardwareSettleTime, 1200u, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET },
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        1,
        "SIM800_Hardware Design_V1.09.pdf",
        "Section 4.2.1 Power on SIM800",
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
                ReviewEvidence{ "Section 4.2.1 Power on SIM800", 25u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 4.2.1 Power on SIM800", 25u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        25u,
        "At least 1.2 seconds"
    },
    {
        "PWRKEY_POWER_ON_SIM800L",
        Category::Init,
        "Pull down PWRKEY to power on SIM800L",
        {{
            { TimeoutKind::HardwareSettleTime, 1000u, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET },
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        1,
        "SIM800L_Hardware Design_V1.00.pdf",
        "Section 4.2.1 Power on SIM800L",
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
                ReviewEvidence{ "Section 4.2.1 Power on SIM800L", 22u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 4.2.1 Power on SIM800L", 22u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        22u,
        "At least 1 second"
    },
    {
        "RESTART_WAIT_STATUS_LOW",
        Category::Init,
        "Wait after STATUS pin goes low before restart",
        {{
            { TimeoutKind::InitDelay, 800u, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET },
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD,
            TIMEOUT_VALUE_PAD
        }},
        1,
        "SIM800_Hardware Design_V1.09.pdf",
        "Section 4.2.3 Restart",
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
                ReviewEvidence{ "Section 4.2.3 Restart", 28u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            {
                "V1.10",
                ReviewStatus::ApprovedPresentEquivalent,
                true,
                ReviewEvidence{ "Section 4.2.3 Restart", 28u, "Auto-filled: timeout equivalent to representative version (V1.12).", "V1.12" }
            },
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD,
            VERSION_REVIEW_PAD
        }},
        2,
        28u,
        "Wait at least 800ms after STATUS pin changes to low level"
    }
}};

inline constexpr std::size_t INIT_TIMEOUTS_COUNT = INIT_TIMEOUTS.size();
static_assert(INIT_TIMEOUTS_COUNT <= MAX_ENTRIES_PER_HEADER,
              "INIT_TIMEOUTS entry count exceeds MAX_ENTRIES_PER_HEADER");

inline constexpr std::array<std::string_view, INIT_TIMEOUTS_COUNT> INIT_TIMEOUTS_COMMAND_INDEX = {{
    "BOOT_TIME_AFTER_PWRKEY",
    "PWRKEY_POWER_OFF",
    "PWRKEY_POWER_ON_SIM800",
    "PWRKEY_POWER_ON_SIM800L",
    "RESTART_WAIT_STATUS_LOW"
}};

inline const CommandEntry* find_init_entry(std::string_view cmd) noexcept {
    auto it = std::lower_bound(INIT_TIMEOUTS_COMMAND_INDEX.begin(), INIT_TIMEOUTS_COMMAND_INDEX.end(), cmd);
    if (it == INIT_TIMEOUTS_COMMAND_INDEX.end() || *it != cmd) return nullptr;
    return &INIT_TIMEOUTS[static_cast<std::size_t>(it - INIT_TIMEOUTS_COMMAND_INDEX.begin())];
}

} // namespace sim800::timeouts::init
