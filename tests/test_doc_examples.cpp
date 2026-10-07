#include <cassert>
#include "sim800_at_timeouts/timeout_types.hpp"
#include "sim800_at_timeouts/at_3gpp.hpp"
#include "sim800_at_timeouts/sms.hpp"
#include "sim800_at_timeouts/http.hpp"

#include "../docs/examples/simple_example.cpp"
#include "../docs/examples/multi_timeout_example.cpp"
#include "../docs/examples/removed_command_example.cpp"
#include "../docs/examples/explicitly_removed_example.cpp"
#include "../docs/examples/not_mentioned_example.cpp"
#include "../docs/examples/same_source_example.cpp"

int main() {
    using namespace sim800::timeouts;
    assert(MS_UNSET == 0xFFFFFFFFu);
    assert(PAGE_UNSET == 0xFFFFFFFFu);
    if (run_simple_example() != 0) return 1;
    if (run_multi_timeout_example() != 0) return 2;
    if (run_removed_command_example() != 0) return 3;
    if (run_explicitly_removed_example() != 0) return 4;
    if (run_not_mentioned_example() != 0) return 5;
    if (run_same_source_example() != 0) return 6;
    return 0;
}
