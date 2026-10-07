#pragma once
#include <cstddef>
#include <cstdint>
#include <string_view>
#include <array>
#include <algorithm>

namespace sim800::timeouts {

using ms_t = std::uint32_t;
inline constexpr ms_t MS_UNSET = 0xFFFFFFFFu;

using page_t = std::uint32_t;
inline constexpr page_t PAGE_UNSET = 0xFFFFFFFFu;

inline constexpr std::size_t MAX_TIMEOUTS_PER_ENTRY  = 8;
inline constexpr std::size_t MAX_VERSION_TIMEOUTS    = 8;
inline constexpr std::size_t MAX_AVAILABLE_VERSIONS  = 8;
inline constexpr std::size_t MAX_VERSION_SPECIFIC    = 8;
inline constexpr std::size_t MAX_VERSION_REVIEWS     = 8;
inline constexpr std::size_t MAX_ENTRIES_PER_HEADER  = 256;

enum class Category : std::uint8_t {
    AtBasic, At3gpp27007, At3gpp27005, Sms, Gprs, Tcpip,
    Http, Ftp, Audio, Stk, Init
};

enum class TimeoutKind : std::uint8_t {
    MaxResponseTime, PromptTimeout, SendTimeout, MaxTimeout,
    MinDelay, MaxWait, BootTime, RetryInterval,
    UrcReportTimeout, InitDelay, HardwareSettleTime
};

enum class ExtractionStatus : std::uint8_t {
    ExtractedFromTable, ExtractedFromText, NotSpecified
};

enum class PresenceStatus : std::uint8_t {
    Present, ExplicitlyRemoved, NotMentioned, NotApplicable
};

enum class ReviewStatus : std::uint8_t {
    ApprovedPresentEquivalent, ApprovedPresentDifferent,
    ApprovedPresentNotMentioned, ApprovedPresentExplicitlyRemoved,
    ApprovedAbsentCommand, ApprovedRemovedCommand,
    PendingReview, RejectedPdfUnavailable, RejectedUncertain,
    NotApplicable
};

struct TimeoutValue {
    TimeoutKind timeout_kind;
    ms_t min_value_ms;
    ms_t max_value_ms;
    ms_t nominal_value_ms;
    ms_t recommended_value_ms;
    ms_t default_value_ms;
};

inline constexpr TimeoutValue TIMEOUT_VALUE_PAD{
    TimeoutKind::MaxResponseTime,
    MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET, MS_UNSET
};

constexpr bool operator==(const TimeoutValue& a, const TimeoutValue& b) noexcept {
    return a.timeout_kind == b.timeout_kind
        && a.min_value_ms == b.min_value_ms
        && a.max_value_ms == b.max_value_ms
        && a.nominal_value_ms == b.nominal_value_ms
        && a.recommended_value_ms == b.recommended_value_ms
        && a.default_value_ms == b.default_value_ms;
}
constexpr bool operator!=(const TimeoutValue& a, const TimeoutValue& b) noexcept { return !(a == b); }

struct VersionEntry {
    std::string_view version;
    std::array<TimeoutValue, MAX_VERSION_TIMEOUTS> timeouts;
    std::uint8_t timeout_count;
    PresenceStatus presence_status;
    ExtractionStatus extraction_status;
    bool source_same_as_representative;
    std::string_view source_document;
    std::string_view source_section;
    bool page_hint_same_as_representative;
    page_t page_hint;
};

struct ReviewEvidence {
    std::string_view section;
    page_t page;
    std::string_view note;
    std::string_view compared_to_version;
};

struct VersionReview {
    std::string_view version;
    ReviewStatus status;
    bool has_evidence;
    ReviewEvidence evidence;
};

inline constexpr VersionReview VERSION_REVIEW_PAD{
    std::string_view{}, ReviewStatus::NotApplicable, false,
    ReviewEvidence{ std::string_view{}, PAGE_UNSET, std::string_view{}, std::string_view{} }
};

struct CommandEntry {
    std::string_view command;
    Category category;
    std::string_view description;
    std::array<TimeoutValue, MAX_TIMEOUTS_PER_ENTRY> timeouts;
    std::uint8_t timeout_count;
    std::string_view source_document;
    std::string_view source_section;
    ExtractionStatus extraction_status_latest;
    PresenceStatus presence_status_latest;
    std::string_view representative_version;
    std::array<std::string_view, MAX_AVAILABLE_VERSIONS> available_in_versions;
    std::uint8_t available_in_versions_count;
    std::array<VersionEntry, MAX_VERSION_SPECIFIC> version_specific;
    std::uint8_t version_specific_count;
    std::array<VersionReview, MAX_VERSION_REVIEWS> version_reviews;
    std::uint8_t version_reviews_count;
    page_t page_hint;
    std::string_view notes;
};

template <typename T, std::size_t N>
constexpr bool array_prefix_equal(const std::array<T, N>& a,
                                  const std::array<T, N>& b,
                                  std::uint8_t count) noexcept {
    for (std::uint8_t i = 0; i < count; ++i) {
        if (!(a[i] == b[i])) return false;
    }
    return true;
}

constexpr bool operator==(const VersionEntry& a, const VersionEntry& b) noexcept {
    if (a.version != b.version) return false;
    if (a.timeout_count != b.timeout_count) return false;
    if (!array_prefix_equal(a.timeouts, b.timeouts, a.timeout_count)) return false;
    if (a.presence_status != b.presence_status) return false;
    if (a.extraction_status != b.extraction_status) return false;
    if (a.source_same_as_representative != b.source_same_as_representative) return false;
    if (a.source_document != b.source_document) return false;
    if (a.source_section != b.source_section) return false;
    if (a.page_hint_same_as_representative != b.page_hint_same_as_representative) return false;
    if (a.page_hint != b.page_hint) return false;
    return true;
}
constexpr bool operator!=(const VersionEntry& a, const VersionEntry& b) noexcept { return !(a == b); }

constexpr bool operator==(const ReviewEvidence& a, const ReviewEvidence& b) noexcept {
    return a.section == b.section && a.page == b.page
        && a.note == b.note && a.compared_to_version == b.compared_to_version;
}
constexpr bool operator!=(const ReviewEvidence& a, const ReviewEvidence& b) noexcept { return !(a == b); }

constexpr bool operator==(const VersionReview& a, const VersionReview& b) noexcept {
    if (a.version != b.version) return false;
    if (a.status != b.status) return false;
    if (a.has_evidence != b.has_evidence) return false;
    if (a.has_evidence && !(a.evidence == b.evidence)) return false;
    return true;
}
constexpr bool operator!=(const VersionReview& a, const VersionReview& b) noexcept { return !(a == b); }

constexpr bool operator==(const CommandEntry& a, const CommandEntry& b) noexcept {
    if (a.command != b.command) return false;
    if (a.category != b.category) return false;
    if (a.description != b.description) return false;
    if (a.timeout_count != b.timeout_count) return false;
    if (!array_prefix_equal(a.timeouts, b.timeouts, a.timeout_count)) return false;
    if (a.source_document != b.source_document) return false;
    if (a.source_section != b.source_section) return false;
    if (a.extraction_status_latest != b.extraction_status_latest) return false;
    if (a.presence_status_latest != b.presence_status_latest) return false;
    if (a.representative_version != b.representative_version) return false;
    if (a.available_in_versions_count != b.available_in_versions_count) return false;
    if (!array_prefix_equal(a.available_in_versions, b.available_in_versions, a.available_in_versions_count)) return false;
    if (a.version_specific_count != b.version_specific_count) return false;
    if (!array_prefix_equal(a.version_specific, b.version_specific, a.version_specific_count)) return false;
    if (a.version_reviews_count != b.version_reviews_count) return false;
    if (!array_prefix_equal(a.version_reviews, b.version_reviews, a.version_reviews_count)) return false;
    if (a.page_hint != b.page_hint) return false;
    if (a.notes != b.notes) return false;
    return true;
}
constexpr bool operator!=(const CommandEntry& a, const CommandEntry& b) noexcept { return !(a == b); }

} // namespace sim800::timeouts
