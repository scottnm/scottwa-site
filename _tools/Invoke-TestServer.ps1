param(
    [switch]$NoNewWindow
    )
    
$pythonArgs = @(
    (Join-Path $PSScriptRoot "local_https_server.py")
    "-d"
    (Join-Path $PSScriptRoot ".." "_site")
)
Start-Process `
    -FilePath "python3.14" `
    -ArgumentList $pythonArgs `
    -NoNewWindow:$NoNewWindow