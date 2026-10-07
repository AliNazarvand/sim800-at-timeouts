#include "sim800_at_timeouts/sms.hpp"

// Demonstrates a command with multiple timeout_kinds (prompt + send +
// max_response_time). Shape-based scan, resilient to data revisions.
int run_multi_timeout_example() {
    using namespace sim800::timeouts;
    for (const auto& e : sms::SMS_TIMEOUTS) {
        if (e.timeout_count < 2) continue;
        bool has_prompt = false;
        bool has_send   = false;
        bool has_mrt    = false;
        for (std::uint8_t i = 0; i < e.timeout_count; ++i) {
            switch (e.timeouts[i].timeout_kind) {
                case TimeoutKind::PromptTimeout:   has_prompt = true; break;
                case TimeoutKind::SendTimeout:     has_send   = true; break;
                case TimeoutKind::MaxResponseTime: has_mrt    = true; break;
                default: break;
            }
        }
        if (has_prompt && has_send && has_mrt) {
            return 0;
        }
    }
    return 1;
}