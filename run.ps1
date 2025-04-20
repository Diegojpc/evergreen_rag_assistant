# run.ps1

# --- Step 1: Load Environment Variables from .env ---
Write-Host "Loading environment variables from .env file..."
try {
    # Check if .env file exists
    if (-not (Test-Path -Path ".env" -PathType Leaf)) {
        throw "'.env' file not found in the current directory."
    }

    # Read the .env file, filter comments and empty lines, and set environment variables
    Get-Content -Path ".env" | Where-Object { $_ -notmatch '^\s*#' -and $_ -match '.+=' } | ForEach-Object {
        # Split on the first '=' sign
        $key, $value = $_ -split '=', 2
        $key = $key.Trim()
        $value = $value.Trim()

        # Basic handling for surrounding quotes (optional but good practice)
        if (($value.StartsWith('"') -and $value.EndsWith('"')) -or ($value.StartsWith("'") -and $value.EndsWith("'"))) {
            $value = $value.Substring(1, $value.Length - 2)
        }

        # Set the environment variable for the current PowerShell process
        # Using [System.Environment]::SetEnvironmentVariable is generally more robust
        [System.Environment]::SetEnvironmentVariable($key, $value, [System.EnvironmentVariableTarget]::Process)
        # Alternatively, for simple cases: $env:$key = $value

        # Write-Host "Set: $key" # Uncomment for debugging
    }
    Write-Host ".env variables loaded into current process environment."

} catch {
    Write-Error "Error loading .env file: $($_.Exception.Message)"
    # Stop the script if .env loading fails
    exit 1
}

# --- Step 2: Verify Essential Environment Variables ---
Write-Host "Verifying required environment variables..."

# Verify SERVER_HOST
if (-not $env:SERVER_HOST) {
    Write-Error "Error: SERVER_HOST environment variable is not set. Ensure it's defined in your .env file."
    exit 1
} else {
    Write-Host "SERVER_HOST = $env:SERVER_HOST"
}

# Verify SERVER_PORT
if (-not $env:SERVER_PORT) {
    Write-Error "Error: SERVER_PORT environment variable is not set. Ensure it's defined in your .env file."
    exit 1
} else {
    Write-Host "SERVER_PORT = $env:SERVER_PORT"
}

# --- Step 3: Run FastAPI server using uvicorn ---
Write-Host "Starting FastAPI server using uvicorn..."

# Determine Python command (python or python3) - adjust if needed
$pythonCommand = "python"
# If 'python3' is your command, uncomment the next line:
# $pythonCommand = "python3"

# Construct the command arguments
$uvicornArgs = "-m uvicorn app.main:app --host $($env:SERVER_HOST) --port $($env:SERVER_PORT) --reload"

# Execute the command
try {
    # Use Invoke-Expression or Start-Process, or simply call python directly
    & $pythonCommand $uvicornArgs.Split(' ')

    # Uvicorn --reload runs until manually stopped (Ctrl+C), so script might end here if not backgrounded.
    # Check $LASTEXITCODE if uvicorn exits immediately (which it shouldn't with --reload unless there's an error)
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Uvicorn failed to start or exited unexpectedly with code $LASTEXITCODE."
    }

} catch {
    Write-Error "Failed to execute uvicorn command: $($_.Exception.Message)"
    exit 1
}

Write-Host "Uvicorn server started (or attempted to start)."