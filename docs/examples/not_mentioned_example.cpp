#include "sim800_at_timeouts/gprs.hpp"

// Demonstrates presence_status_latest == NotMentioned.
// Shape-based scan; if the gprs category no longer carries such an
// entry, fall back to at_3gpp.
#include "sim800_at_timeouts/at_3gpp.hpp"

int run_not_mentioned_example() {
    using namespace sim800::timeouts;
    for (const auto& e : gprs::GPRS_TIMEOUTS) {
        if (e.presence_status_latest == PresenceStatus::NotMentioned) {
            return 0;
        }
    }
    for (const auto& e : at_3gpp::AT_3GPP_TIMEOUTS) {
        if (e.presence_status_latest == PresenceStatus::NotMentioned) {
            return 0;
        }
    }
    return 1;
}