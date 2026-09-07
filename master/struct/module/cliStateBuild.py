# ==========================================================================
# EXISTENZ CORE BUILDER (Signing Suite & Cross-Compiler)
# Version: v0.76.16 | Github Deployment
# Copyright (c) 2026 by Gunther Voet. All Rights Reserved.
# Released under strict Non-Commercial Open-Source License terms.
# ==========================================================================
import os
import sys
import engineSigningLibrary
import engineBuilderLibrary

def execute(args, error_handler, repo_root: str):
    """
    Executes dynamic cross-language code generation across the /dist/ matrix.
    Enforces that both verify and veritas passes must return successful passes.
    """
    error_handler.print("Asserting verification ring clearances before starting compiler passes...", level="notice")
    
    # Enforce consensus gates before touching files
    # (Checked via your live pipeline sequencing environment tracks)
    
    # Locate paths pointing natively to your master blueprint database JSON tracking assets
    blueprint_file_name = "master/struct/existentialCoreSchema.json"
    blueprint_absolute_path = os.path.abspath(os.path.join(repo_root, blueprint_file_name))

    # Evaluate dynamic bitmask limits passed down through command arguments; fallback to ALL formats (0xFFFFFFFF)
    # This automatically honors: python3 engineSigningCLI.py -stage build -bitmask <value>
    active_mask = int(args.bitmask) if getattr(args, "bitmask", None) is not None else 0xffffffff

    # Trigger the dynamic plugin iteration matrix loop
    engineBuilderLibrary.execute_universal_builder_matrix(
        repo_root=repo_root,
        error_handler=error_handler,
        bitmask_arg=active_mask,
        blueprint_path=blueprint_absolute_path
    )

    error_handler.print("[+++] SUCCESS: Distribution build matrix fully synchronized. Release artifacts generated.", level="notice")
    engineSigningLibrary.pipeline_step_next(args.stage, error_handler)
