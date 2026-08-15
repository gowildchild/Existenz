name: Existenz - Check Ingest Export Divide
# This routine does everything what it should
# do on the Guthub of Existenz. This gives 
# confidence that the structure is not 
# tampered with, while kept at the standard of
# the science that it is built upon. 

on:
  push:
    branches: [ "main", "master", "develop" ]
  pull_request:
    branches: [ "main", "master", "develop" ]

jobs:
  validate-and-compile:
    runs-on: ubuntu-latest

    steps:
    - name: Existenz - Checkout Code Blueprint
      uses: actions/checkout@v4

    - name: Existenz - Initialize Python Runtime
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    # Step 3: Determine Operational Mode from the Lockfile
    - name: Existenz - Installing Dependencies
      run: pip install pyyaml cryptography    
    - name: Existenz - Checking Myself 
      id: mode_check
      run: |
        if [ -f "existenzStruct/.existentialLock" ]; then
          # Read the first line, strip whitespace, and convert to lowercase
          MODE=$(head -n 1 existenzStruct/.existentialLock | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
          echo "Found lockfile. Selected Mode: $MODE"
        else
          MODE="compile"
          echo "No lockfile detected. Defaulting to Mode: $MODE"
        fi
        # Save the mode variable to the GitHub Actions environment map
        echo "RUN_MODE=$MODE" >> $GITHUB_ENV

    # Step 4: Standalone Cryptographic Hash Audit (Absolute Root Context)
    - name: Existenz - Checksum Validation
      if: env.RUN_MODE != 'locked'
      run: |
        # Inject the physical repository root natively into Python's search path
        # This allows absolute paths (existenzStruct.master...) to resolve flawlessly!
        PYTHONPATH="${GITHUB_WORKSPACE}" python existenzStruct/tools/check_integrity.py

    # Step 5: Execute Suite and Compile Structures (Skipped if fully locked)
    - name: Compiling Pristine Universal Structures - Existenz
      if: env.RUN_MODE != 'locked'
      run: |
        python existenzStruct/tools/core_build.py -step compile

    # Step 6: Conditional Repository Sync Phase (ONLY fires in compile mode)
    - name: Existenz - git commit and push to repo
      if: env.RUN_MODE == 'compile'
      run: |
        echo "[*] Compile mode active. Synchronizing repository files..."
        git config --global user.name "Existenz Platform Bot"
        git config --global user.email "32355099+gowildchild@users.noreply.github.com"
      
        cp existenzStruct/master/existentialCore.py dist/
        cp existenzStruct/master/existentialCoreThreat.py dist/
        
        git add dist/
        
        if git diff --staged --quiet; then
          echo "[+] No structural changes detected. Skipping push."
        else
          git commit -m "Existenz: universal cross-language structures"
          git push
        fi      

    # Step 7: Assert Schema and Code Generation Success (Skipped if fully locked)
    - name: Existenz - Test Universal Data Structures
      if: env.RUN_MODE != 'locked'
      run: |
        test -f dist/existentialCore.json
        test -f dist/existentialCore.xml
        test -f dist/existentialCoreThreat.json
        test -f dist/existentialCoreThreat.xml        
        test -f dist/rust/single/existentialCore.rs
        test -f dist/cpp/single/existentialCore.hpp
        test -f dist/php/single/existentialCore.php
        test -f dist/perl/single/existentialCore.pm
        echo "[+] Compilation and schema verification successful."
        
    # Step 8: Log Output for Integrity Check Mode
    - name: Existenz - Terminate Integrity Check 
      if: env.RUN_MODE == 'integritycheck'
      run: |
        echo "[*] Pipeline Status: Mode [INTEGRITYCHECK] complete."
        echo "[+] Results: System signatures and structures verified clean."
        echo "[+] Notice: Repository commit bypassed intentionally to protect active deployment."
