#include "sim800_at_timeouts/http.hpp"
#include <string_view>

// Demonstrates a command whose representative_version is not the
// global latest (V1.12). Shape-based scan.
int run_removed_command_example() {
    using namespace sim800::timeouts;
    for (const auto& e : http::HTTP_TIMEOUTS) {
        if (e.representative_version != "V1.12") {
            return 0;
        }
    }
    return 1;
}