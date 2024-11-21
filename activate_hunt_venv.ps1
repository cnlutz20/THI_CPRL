# Navigate to the Scripts folder
Set-Location -Path "C:\Users\clutz\hunt_env\Scripts"

# Run the activation script (Activate.ps1)
.\Activate.ps1
Write-Host "Ran Activation file"

# Return to the original folder
Set-Location -Path "C:\Users\clutz\Projects"
Write-Host "Returned to C:\Users\clutz\Projects"

# Pause the script (similar to 'pause' in batch files)
Write-Host "Press any key to continue..." -NoNewline
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")