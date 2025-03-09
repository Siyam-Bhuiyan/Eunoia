# To run this script:
# Option 1 - For current user only (recommended):
#   1. Open PowerShell (no admin required)
#   2. Run: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
#   3. Navigate to script directory: cd c:\Users\User\Documents\Eunoia\Eunoia
#   4. Run the script: .\initialize_conda.ps1
#
# Option 2 - For all users (requires admin):
#   1. Open PowerShell as Administrator
#   2. Run: Set-ExecutionPolicy RemoteSigned
#   3. Navigate to script directory: cd c:\Users\User\Documents\Eunoia\Eunoia
#   4. Run the script: .\initialize_conda.ps1

# Try to set execution policy for current user if not already set
try {
    $currentPolicy = Get-ExecutionPolicy -Scope CurrentUser
    if ($currentPolicy -eq "Restricted") {
        Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force
        Write-Host "Execution policy updated for current user"
    }
} catch {
    Write-Host "Please run 'Set-ExecutionPolicy -Scope CurrentUser RemoteSigned' first"
    exit 1
}

# Initialize conda for PowerShell
# First, check if conda is in PATH
$condaPath = (Get-Command conda -ErrorAction SilentlyContinue).Source
if (-not $condaPath) {
    $possiblePaths = @(
        "$env:USERPROFILE\Anaconda3",
        "$env:USERPROFILE\Miniconda3",
        "C:\ProgramData\Anaconda3",
        "C:\ProgramData\Miniconda3"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            # Initialize conda
            & "$path\shell\condabin\conda-hook.ps1"
            # Activate conda
            & "$path\Scripts\activate"
            
            # Verify conda is working
            $condaTest = (Get-Command conda -ErrorAction SilentlyContinue).Source
            if ($condaTest) {
                Write-Host "Conda initialized and verified successfully!" -ForegroundColor Green
                Write-Host "You can now use conda commands in this PowerShell session" -ForegroundColor Green
                Write-Host "Try running: conda --version" -ForegroundColor Cyan
            } else {
                Write-Host "Conda initialization completed but verification failed." -ForegroundColor Yellow
                Write-Host "Please restart PowerShell and try again." -ForegroundColor Yellow
                Write-Host "If the issue persists, reinstall Anaconda/Miniconda with 'Add to PATH' option" -ForegroundColor Yellow
            }
            exit 0
        }
    }
    
    Write-Host "Error: Conda installation not found. Please install Anaconda or Miniconda first."
    Write-Host "Download from: https://docs.conda.io/en/latest/miniconda.html"
    Write-Host "IMPORTANT: During installation, make sure to check the option 'Add to PATH'"
    exit 1
}
