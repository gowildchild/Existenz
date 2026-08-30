# ==========================================================================
# THE EXISTENZ PLATFORM (TEMPORARY ARCHITECTURAL INITIALIZATION BOOT GUARD)
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved. 
# ==========================================================================
# FILE: existenzStruct/tools/boot_guard.py
#
import os
import sys

# 1. Capture the absolute workspace repository root directory context
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# 2. FORCEFULLY UNLOAD PYTHON'S CACHED BUILT-IN "STRUCT" INTERFACE
# This breaks the "struct is not a package" loop cleanly.
# if 'struct' in sys.modules:
#     del sys.modules['struct']
# 3. FIX: Only remove the specific dynamic wrapper conflict without breaking standard libraries
# sys.path = [p for p in sys.path if not p.endswith('lib-dynload')]
sys.modules['struct'] = None

# 4. Inject your custom isolated root at position 0 to force priority resolution
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
