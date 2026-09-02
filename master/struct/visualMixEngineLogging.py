# ==========================================================================
# VisualMIX Engine : Logging
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================

import os
import sys
import time
from typing import Dict, Any

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPO_GITHUB = os.environ.get('GITHUB_ACTIONS') == 'true'

class visualmixErrorHandler:
    """Handles script termination and formats logs cleanly for both Local and GitHub environments."""
    ERR_GENERAL          = 1
    ERR_ARGPARSE         = 2
    ERR_MISSING_CORE     = 4
    ERR_MISSING_LOCAL    = 8
    ERR_MISSING_CONFIG   = 16
    ERR_MISSING_FILE     = 32
    ERR_MISSING_MANIFEST = 33
    ERR_MISSING_SIGN     = 62
    ERR_MISSING_KEY      = 63
    ERR_KEY              = 64
    ERR_KEY_DRIFTING     = 65
    ERR_KEY_VALUE        = 66
    ERR_KEY_FORMAT       = 67
    ERR_KEY_EXCEPTION    = 68
    ERR_MISSING_EXECUTE  = 126
    ERR_MISSING_EXE      = 127
    ERR_UNKNOWN          = 254
    ERR_OUT_OF_RANGE     = 255
    
    # Decoupled Mapping: (Color/Style Prefix, GitHub Command Prefix, GitHub Allowed Flag)
    ERR_MAP = {
        "error":   ("\033[1;31m[!] ERROR",   "::error", True),
        "warning": ("\033[1;33m[?] Warning", "::warning", True),
        "notice":  ("\033[1;36m[+] Notice",  "::notice", True),
        "debug":   ("\033[1;35m[-] Debug",   "::debug", True),
        "info":    ("\033[0;37m[ ] Info",    "  Info", True),
        "local":   ("\033[0;37m[ ] Local",   "", False)
    }

    def __init__(self, custom_struct: dict = None, custom_post: str, log_file_path: str = None):
        self.custom_post = custom_post if custom_post is not None else "_ERR"
        self.default_struct = {
            v: k for k, v in vars(self.__class__).items() 
            if k.startswith(self.custom_post) and isinstance(v, int)
        }
        self.current_errors = custom_struct if custom_struct is not None else self.default_struct
        self.log_file_path = log_file_path
        
        if self.log_file_path:
            # Open disk stream completely clear of ANSI overhead
            with open(self.log_file_path, "w", encoding="utf-8") as f:
                f.write(f"--- VisualMixEngineLogging.py ({int(time.time())}) ---\n")

    def _write_to_disk_handler(self, plain_text: str):
        """Dedicated file writer handler ensuring pure plain-text isolation."""
        if not self.log_file_path:
            return
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.write(plain_text + "\n")
        except Exception:
            pass

    def _write_to_screen_handler(self, formatted_text: str):
        """Dedicated standard out writer handler maintaining vibrant colors."""
        print(formatted_text)

    def load_dynamic_struct(self, dynamic_struct: dict):
        """Allows alternative orchestrators to hot-swap error structures mid-execution."""
        self.current_errors = dynamic_struct if dynamic_struct is not None else self.default_struct

    def notice(self, level: str, message: str, exit_code: int = None, details: list = None):
        """Centralized logging method handling independent stream separation for file and screen."""
        notice_style, notice_github, notice_github_allowed = self.ERR_MAP.get(level, self.ERR_MAP["info"])
        
        if REPO_GITHUB:
            indent = " " * (len(level) + 2)
            if not notice_github_allowed:
                return

            no_details = level in ["info", "debug"] or not exit_code
            meta = "" if no_details else f" file=visualMixEngineLogging.py::[Exit Code {exit_code}]"
            
            # Send plain text to file stream, formatted blocks to workflow runner screen stream
            self._write_to_disk_handler(f"{level.upper()}{meta}: {message}")
            self._write_to_screen_handler(f"{notice_github}{meta}::{message}")
            
            if details:
                for line in details:
                    self._write_to_disk_handler(f"{indent}{line}")
                    self._write_to_screen_handler(f"{indent}{line}")
        else:
            indent = " " * 10
            if exit_code:
                err_label = self.current_errors.get(exit_code, "ERR_UNKNOWN")
                plain_label = f"_{err_label} ({exit_code})"
            else:
                plain_label = ""
                
            # Stream 1: Assemble clean, uncolored plain text message for the disk handler
            disk_body = f"[{level.upper()}]{plain_label}: {message}"
            self._write_to_disk_handler(disk_body)
            
            # Stream 2: Assemble localized ANSI visual string for the screen handler
            screen_body = f"  {notice_style}{plain_label}: {message}\033[0m"
            self._write_to_screen_handler(screen_body)
            
            if details:
                for line in details:
                    self._write_to_disk_handler(f"{indent}{line}")
                    self._write_to_screen_handler(f"{indent}{line}")

        if exit_code is not None:
            sys.exit(exit_code)

def main():
    parser = argparse.ArgumentParser(
        description="Existenz cross-compile builder and private signing suite"
    )
    parser.add_argument(
        "-step", "--step",
        choices=["verify","check", "sign", "compile"],
        required=True,
        help="Specify the pipeline stage to run. 'check'=audit, 'sign'=matrix mapping, 'compile'=cross-compile."
    )
    parser.add_argument(
        "-dist", "--dist",
        choices=["existenzStruct","dist"],
        default="existenzStruct",
        help="Distro to sign"
    )
    parser.add_argument(
        "-r", "--run", 
        choices=["WET", "dry"], 
        default="WET",
        help="Execution strategy state constraint. 'dry' bypasses filesystem modifications."
    )
    args = parser.parse_args()
    pub_ver = existentialCoreVersion or None
    if pub_ver != int_ver:
        pub_ver = existentialCoreVersion + "/" + int_ver
    else:
        pub_ver = int_ver


if __name__ == "__main__":
    main()

# error_handler = visualmixErrorHandler(log_file_path=os.path.join(REPO_ROOT, "visualMixEngineLogger.log"))
