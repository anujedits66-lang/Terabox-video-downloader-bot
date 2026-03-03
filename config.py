import os
from dotenv import load_dotenv

load_dotenv()

# ===== Required =====
BOT_TOKEN: str = os.environ["8755130382:AAF9jzZEYZkoBiKTFFcqIQUaZO3GFL7QL_A"]   # Secure rakha gaya

# ===== 4GB User Session (Filled) =====
API_ID: int = 34724970
API_HASH: str = "f240eae7c60e8e30c17203ab0e052f7e"
SESSION_STRING: str = "BQIR3GoAaByWwNVXoLflX4wyOXmPgTxkQ2UtchTCvGRxaSJkL0DPH9aw9wTSnPf4rS6nPpy-I0EVu0sowr_m4Iotb2ohQbccmE-thpuG0vtUjQkSTD_HlGgiaMekMlkmRgx7WIC3L3pLA9uPhXLB3aj6PpZvqv6YNrzBuv_oyoCWtrdN-ulRpw6gLUif0twLOxtJyuxHYONk3iaEmlyMxVmJxHy1eScuco573Z7mtTRq2WqS-hjgK5JRLW6NBsfb1rmXPYB6wI0LaRKxd7ZH_2S4iGuCoYlFkDsfJMBYJ_hi55hkyC_puFfyHLkVL-w7vHcBgFKMHG12_oIRBE_SyIfwOsTruAAAAAHAT8hYAA"

# ===== Upload Limits =====
_4GB = 4 * 1024 ** 3
_2GB = 2 * 1024 ** 3

MAX_UPLOAD_SIZE: int = _4GB
BOT_API_LIMIT: int = 50 * 1024 ** 2

# ===== Other Settings =====
CACHE_TTL: int = 7200
LOG_LEVEL: str = "INFO"
