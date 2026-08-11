# ==========================================================================
# THE EXISTENZ PLATFORM (INITIALIZATION BOOT GUARD)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# ==========================================================================
# FILE: existenzStruct/tools/boot_guard.py
#
import os
import sys

# 1. Dynamically capture the repository root directory context
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# 2. FORCEFULLY UNLOAD PYTHON'S INTERNAL STANDARD LIBRARY STRUCT REFERENCE
# If the interpreter has pre-cached its built-in 'struct' package, purge it!
if 'struct' in sys.modules:
    del sys.modules['struct']

# 3. Strip away system dynamic library loading paths that default to built-ins
sys.path = [p for p in sys.path if not p.endswith('lib-dynload') and 'python3.' not in p]

# 4. Inject your custom isolated root at position 0 to force priority resolution
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
