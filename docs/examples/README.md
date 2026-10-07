# Canonical Examples

Each pair `*.yaml` + `*.cpp` demonstrates one structural case of the
database. Every `.cpp` exports `int run_<name>_example()` (no `main`), so the
files can be `#include`d from `tests/test_doc_examples.cpp`.

Each `.yaml` file contains a `metadata:` block (with `description`,
`schema_version`, `database_version`, `review_scope`, `pending_versions`,
`extracted_from`) and an `entries:` list with at least one `CommandEntry`.

| file | demonstrates |
|------|--------------|
| `simple_example.yaml` / `.cpp` | Single `max_response_time` — `.cpp` scans `at_3gpp` for the shape. |
| `multi_timeout_example.yaml` / `.cpp` | Three `timeout_kind`s on `AT+CMGS` (prompt / send / max_response). |
| `removed_command_example.yaml` / `.cpp` | `representative_version != global_latest` (`AT+HTTPACTION`, removed in V1.12). |
| `explicitly_removed_example.yaml` / `.cpp` | `presence_status: explicitly_removed` in `version_specific`. |
| `not_mentioned_example.yaml` / `.cpp` | `presence_status: not_mentioned` (`AT+CGDCONT`). |
| `same_source_example.yaml` / `.cpp` | `source_same_as_representative: true` and `page_hint_same_as_representative: true`. |
