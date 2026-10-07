#include "sim800_at_timeouts/at_3gpp.hpp"

// Demonstrates a command with a single max_response_time.
// Rather than pin one command, we scan the category for the shape,
// so this example is resilient to data revisions.
int run_simple_example() {
    using namespace sim800::timeouts;
    for (const auto& e : at_3gpp::AT_3GPP_TIMEOUTS) {
        if (e.timeout_count == 1 &&
            e.timeouts[0].timeout_kind == TimeoutKind::MaxResponseTime &&
            e.timeouts[0].max_value_ms != MS_UNSET) {
            return 0;
        }
    }
    return 1;
}