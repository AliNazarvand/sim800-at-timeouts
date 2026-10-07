# SIM800 AT Timeouts

Static database of timeout values, Max Response Time, and Default Values
for SIM800-series AT commands, extracted exclusively from official PDF documentation.

## Scope

This project is **only** a static database. It is not a module driver,
AT command library, or hardware controller.

## Design Decisions

- `version_specific` models per-version timeout differences.
- `global_latest` is the newest version in `versions.yaml` (V1.12).
- `representative_version` is the newest version containing the command.
- All timeout values are in milliseconds.
- `default_value_ms` is sourced exclusively from PDF text.

## Building

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build
```

## License

MIT
