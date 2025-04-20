# Export environment variables from .env:
Get-Content .env | ForEach-Object {
    if (-not ($_ -match "^\s*#") -and $_ -match "\S") {
        $key, $value = $_ -split '=', 2
        [Environment]::SetEnvironmentVariable($key, $value, [System.EnvironmentVariableTarget]::Process)
    }
}

# Verify if SERVER_HOST environment variable exists
if (-not [Environment]::GetEnvironmentVariable("SERVER_HOST")) {
    Write-Error "Error: SERVER_HOST environment variable is not set"
    exit 1
}

# Verify if SERVER_PORT environment variable exists
if (-not [Environment]::GetEnvironmentVariable("SERVER_PORT")) {
    Write-Error "Error: SERVER_PORT environment variable is not set"
    exit 1
}

# Run FastAPI server using uvicorn:
python -m uvicorn app.main:app --host $env:SERVER_HOST --port $env:SERVER_PORT --reload