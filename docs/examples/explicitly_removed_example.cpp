#include "sim800_at_timeouts/timeout_types.hpp"

// Self-contained: demonstrates that PresenceStatus::ExplicitlyRemoved
// is a distinct enumerator from PresenceStatus::Present.
int run_explicitly_removed_example() {
    using namespace sim800::timeouts;
    return PresenceStatus::ExplicitlyRemoved != PresenceStatus::Present ? 0 : 1;
}