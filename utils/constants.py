DETECTOR_ID_DICT = {
    "1" : "NewMatchPathValueDetector",
    "2" : "NewMatchPathValueComboDetector",
    "3" : "CharsetDetector",
    "4" : "EntropyDetector",
    "5" : "ValueRangeDetector",
    "6" : "EventFrequencyDetector",
    "7" : "EventSequenceDetector"
}

POSSIBLE_TIMESTAMP_FORMATS = [
    "%Y-%m-%d %H:%M:%S",       # Common ISO-like format: '2023-10-02 14:30:59'
    "%d/%b/%Y:%H:%M:%S %z",    # Apache/Nginx logs: '02/Oct/2023:14:30:59 +0000'
    "%Y-%m-%dT%H:%M:%S",       # ISO 8601 format: '2023-10-02T14:30:59'
    "%Y-%m-%d %H:%M:%S.%f",    # With microseconds: '2023-10-02 14:30:59.123456'
    "%d/%m/%Y %H:%M:%S",       # European format: '02/10/2023 14:30:59'
    "%a, %d %b %Y %H:%M:%S %Z",# RFC 1123 format: 'Mon, 02 Oct 2023 14:30:59 GMT'
    "%Y/%m/%d %H:%M:%S",       # Slashed date format: '2023/10/02 14:30:59'
    "%m/%d/%Y %I:%M:%S %p",    # US format with AM/PM: '10/02/2023 02:30:59 PM'
    "%b %d %H:%M:%S",          # Syslog format: 'Oct 02 14:30:59'
    "%Y%m%d %H:%M:%S",         # Compact format: '20231002 14:30:59'
    "%Y-%m-%d",                # Date only: '2023-10-02'
    "%H:%M:%S",                # Time only: '14:30:59'
    "%Y%m%dT%H%M%S",           # Basic ISO 8601: '20231002T143059'
    "%Y-%m-%dT%H:%M:%S.%fZ",   # ISO 8601 with microseconds and 'Z' for UTC: '2023-10-02T14:30:59.123456Z'
    "%d-%b-%Y %H:%M:%S",       # Day-Month-Year format: '02-Oct-2023 14:30:59'
    "%Y%m%d",                  # Date only without separators: '20231002'
    "%d-%m-%Y",                # European date format: '02-10-2023'
    "%a %b %d %H:%M:%S %Y",    # C-style asctime format: 'Mon Oct 02 14:30:59 2023'
]

POSSIBLE_TIMESTAMP_PATHS = [
    "/model/time",
    "/model/@timestamp/time",
    "/model/with_data/time",
    "/model/type/execve/time",
    "/model/type/proctitle/time",
    "/model/type/syscall/time",
    "/model/type/path/time",
    "/model/type/login/time",
    "/model/type/sockaddr/time",
    "/model/type/unknown/time",
    "/model/type/cred_refr/time",
    "/model/type/user_start/time",
    "/model/type/user_acct/time",
    "/model/type/user_auth/time",
    "/model/type/user_login/time",
    "/model/type/cred_disp/time",
    "/model/type/service_start/time",
    "/model/type/service_stop/time",
    "/model/type/user_end/time",
    "/model/type/user_cmd/time",
    "/model/type/cred_acq/time",
    "/model/type/avc/time",
    "/model/type/user_bprm_fcaps/time",
    "/model/datetime"
]