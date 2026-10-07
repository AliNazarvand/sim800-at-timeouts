# Coverage Report

## Section 1 — Extracted value coverage

Coverage is computed **only over commands with
`presence_status_latest: present`**, per acceptance criteria.
Commands marked `not_mentioned` are excluded from the
denominator (the PDF does not specify a timeout for them).

| file | present | extracted | not_extracted | coverage |
|------|--------:|----------:|--------------:|---------:|
| at_3gpp.yaml | 4 | 4 | 0 | 100.0% |
| at_basic.yaml | 0 | 0 | 0 | n/a |
| audio.yaml | 0 | 0 | 0 | n/a |
| ftp.yaml | 2 | 2 | 0 | 100.0% |
| gprs.yaml | 0 | 0 | 0 | n/a |
| http.yaml | 1 | 1 | 0 | 100.0% |
| init.yaml | 5 | 5 | 0 | 100.0% |
| sms.yaml | 4 | 4 | 0 | 100.0% |
| stk.yaml | 0 | 0 | 0 | n/a |
| tcpip.yaml | 4 | 4 | 0 | 100.0% |
| **TOTAL** | 20 | 20 | 0 | 100.0% |

## Section 2 — Version review status

| file | command | representative | approved_* | pending_* | rejected_* |
|------|---------|----------------|-----------|-----------|-----------|
| at_3gpp.yaml | AT+CGACT | V1.12 | V1.01, V1.10 | - | - |
| at_3gpp.yaml | AT+CGATT | V1.12 | V1.01, V1.10 | - | - |
| at_3gpp.yaml | AT+CGREG | V1.12 | V1.01, V1.10 | - | - |
| at_3gpp.yaml | AT+COPS | V1.12 | V1.01, V1.10 | - | - |
| at_3gpp.yaml | AT+CPIN | V1.12 | V1.01, V1.10 | - | - |
| at_3gpp.yaml | AT+CREG | V1.12 | V1.01, V1.10 | - | - |
| at_3gpp.yaml | AT+CSQ | V1.12 | V1.01, V1.10 | - | - |
| at_3gpp.yaml | AT+CGSN | V1.12 | V1.01, V1.10 | - | - |
| at_3gpp.yaml | AT+CMEE | V1.12 | V1.01, V1.10 | - | - |
| at_3gpp.yaml | AT+CPMS | V1.12 | V1.01, V1.10 | - | - |
| at_3gpp.yaml | AT+CNMI | V1.12 | V1.01, V1.10 | - | - |
| at_basic.yaml | AT | V1.12 | V1.01, V1.10 | - | - |
| audio.yaml | AT+CHFA | V1.12 | V1.01, V1.10 | - | - |
| audio.yaml | AT+CLVL | V1.12 | V1.01, V1.10 | - | - |
| audio.yaml | AT+CMIC | V1.12 | V1.01, V1.10 | - | - |
| audio.yaml | AT+CMUT | V1.12 | V1.01, V1.10 | - | - |
| audio.yaml | AT+CRSL | V1.12 | V1.01, V1.10 | - | - |
| audio.yaml | AT+VTS | V1.12 | V1.01, V1.10 | - | - |
| ftp.yaml | AT+FTPGET | V1.12 | V1.01, V1.10 | - | - |
| ftp.yaml | AT+FTPPUT | V1.12 | V1.01, V1.10 | - | - |
| gprs.yaml | AT+CGDCONT | V1.12 | V1.01, V1.10 | - | - |
| http.yaml | AT+HTTPACTION | V1.10 | V1.01, V1.12 | - | - |
| http.yaml | AT+HTTPINIT | V1.10 | V1.01, V1.12 | - | - |
| http.yaml | AT+HTTPREAD | V1.10 | V1.01, V1.12 | - | - |
| init.yaml | BOOT_TIME_AFTER_PWRKEY | V1.12 | V1.01, V1.10 | - | - |
| init.yaml | PWRKEY_POWER_OFF | V1.12 | V1.01, V1.10 | - | - |
| init.yaml | PWRKEY_POWER_ON_SIM800 | V1.12 | V1.01, V1.10 | - | - |
| init.yaml | PWRKEY_POWER_ON_SIM800L | V1.12 | V1.01, V1.10 | - | - |
| init.yaml | RESTART_WAIT_STATUS_LOW | V1.12 | V1.01, V1.10 | - | - |
| sms.yaml | AT+CMGD | V1.12 | V1.01, V1.10 | - | - |
| sms.yaml | AT+CMGF | V1.12 | V1.01, V1.10 | - | - |
| sms.yaml | AT+CMGL | V1.12 | V1.01, V1.10 | - | - |
| sms.yaml | AT+CMGR | V1.12 | V1.01, V1.10 | - | - |
| sms.yaml | AT+CMGS | V1.12 | V1.01, V1.10 | - | - |
| stk.yaml | AT+STKCALL | V1.12 | V1.01, V1.10 | - | - |
| stk.yaml | AT+STKMENU | V1.12 | V1.01, V1.10 | - | - |
| tcpip.yaml | AT+CIFSR | V1.12 | V1.01, V1.10 | - | - |
| tcpip.yaml | AT+CIICR | V1.12 | V1.01, V1.10 | - | - |
| tcpip.yaml | AT+CIPCLOSE | V1.12 | V1.01, V1.10 | - | - |
| tcpip.yaml | AT+CIPSHUT | V1.12 | V1.01, V1.10 | - | - |
| tcpip.yaml | AT+CIPSEND | V1.12 | V1.01, V1.10 | - | - |
| tcpip.yaml | AT+CIPSTART | V1.12 | V1.01, V1.10 | - | - |
| tcpip.yaml | AT+CIPMUX | V1.12 | V1.01, V1.10 | - | - |
| tcpip.yaml | AT+CSTT | V1.12 | V1.01, V1.10 | - | - |
| tcpip.yaml | AT+CIPSTATUS | V1.12 | V1.01, V1.10 | - | - |

## Section 3 — timeout_kind coverage

Covered: boot_time, hardware_settle_time, init_delay, max_response_time, max_timeout, prompt_timeout, send_timeout, urc_report_timeout

Gaps: max_wait, min_delay, retry_interval
