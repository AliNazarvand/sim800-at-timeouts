# Data Corrections Report (Phase-9)

Mode: APPLY
Total AT entries: 39
  kept           : 33
  changed (ms)   : 1
  not_mentioned  : 0
  skipped        : 5

| file | command | V1.01 | V1.10 | V1.12 | current_ms | current_pres | action |
|------|---------|-------|-------|-------|-----------:|--------------|--------|
| at_3gpp.yaml | AT+CGACT | present=150000 | no_mrt_label | present=150000 | 150000 | present | keep |
| at_3gpp.yaml | AT+CGATT | present=10000 | present=75000 | present=75000 | 75000 | present | keep |
| at_3gpp.yaml | AT+CGREG | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| at_3gpp.yaml | AT+COPS | unparseable | unparseable | unparseable | 120000 | present | skip_unparseable |
| at_3gpp.yaml | AT+CPIN | present=5000 | present=5000 | present=5000 | 5000 | present | keep |
| at_3gpp.yaml | AT+CREG | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| at_3gpp.yaml | AT+CSQ | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| at_3gpp.yaml | AT+CGSN | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| at_3gpp.yaml | AT+CMEE | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| at_3gpp.yaml | AT+CPMS | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| at_3gpp.yaml | AT+CNMI | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| audio.yaml | AT+CHFA | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| audio.yaml | AT+CLVL | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| audio.yaml | AT+CMIC | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| audio.yaml | AT+CMUT | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| audio.yaml | AT+CRSL | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| audio.yaml | AT+VTS | unparseable | unparseable | unparseable | None | not_mentioned | skip_unparseable |
| ftp.yaml | AT+FTPGET | present=60000 | present=75000 | present=75000 | 75000 | present | keep |
| ftp.yaml | AT+FTPPUT | present=60000 | present=75000 | present=75000 | 75000 | present | keep |
| gprs.yaml | AT+CGDCONT | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| http.yaml | AT+HTTPACTION | unparseable | unparseable | unparseable | 60000 | present | skip_unparseable |
| http.yaml | AT+HTTPINIT | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| http.yaml | AT+HTTPREAD | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| sms.yaml | AT+CMGD | present=5000 | present=5000 | present=5000 | 5000 | present | keep |
| sms.yaml | AT+CMGF | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| sms.yaml | AT+CMGL | present=20000 | present=20000 | present=20000 | 20000 | present | keep |
| sms.yaml | AT+CMGR | no_mrt_label | present=5000 | present=5000 | 5000 | present | keep |
| sms.yaml | AT+CMGS | present=60000 | present=60000 | present=60000 | None | present | set_ms |
| stk.yaml | AT+STKCALL | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| stk.yaml | AT+STKMENU | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| tcpip.yaml | AT+CIFSR | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| tcpip.yaml | AT+CIICR | no_mrt_label | present=85000 | present=85000 | 85000 | present | keep |
| tcpip.yaml | AT+CIPCLOSE | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| tcpip.yaml | AT+CIPSHUT | no_mrt_label | present=65000 | present=65000 | 65000 | present | keep |
| tcpip.yaml | AT+CIPSEND | no_mrt_label | unparseable | unparseable | None | present | skip_unparseable |
| tcpip.yaml | AT+CIPSTART | no_mrt_label | unparseable | unparseable | 160000 | present | skip_unparseable |
| tcpip.yaml | AT+CIPMUX | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| tcpip.yaml | AT+CSTT | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
| tcpip.yaml | AT+CIPSTATUS | no_mrt_label | not_mentioned | not_mentioned | None | not_mentioned | keep |
