#include <cassert>
#include <string_view>
#include "sim800_at_timeouts/timeout_types.hpp"
#include "sim800_at_timeouts/sms.hpp"
#include "sim800_at_timeouts/http.hpp"
#include "sim800_at_timeouts/at_3gpp.hpp"

int main() {
    using namespace sim800::timeouts;

    // Overflow guards: use fully-qualified names for COUNT constants
    // because they live in their own category namespaces.
    static_assert(sim800::timeouts::sms::SMS_TIMEOUTS_COUNT
                      <= MAX_ENTRIES_PER_HEADER, "SMS overflow");
    static_assert(sim800::timeouts::http::HTTP_TIMEOUTS_COUNT
                      <= MAX_ENTRIES_PER_HEADER, "HTTP overflow");
    static_assert(sim800::timeouts::at_3gpp::AT_3GPP_TIMEOUTS_COUNT
                      <= MAX_ENTRIES_PER_HEADER, "AT_3GPP overflow");

    assert(MS_UNSET == 0xFFFFFFFFu);
    assert(PAGE_UNSET == 0xFFFFFFFFu);

    // Finders use category-qualified calls; the prefix resolves via
    // "using namespace sim800::timeouts".
    auto* s = sms::find_sms_entry("AT+CMGS");
    auto* h = http::find_http_entry("AT+HTTPACTION");
    auto* a = at_3gpp::find_at_3gpp_entry("AT+CSQ");
    (void)s; (void)h; (void)a;
    return 0;
}
