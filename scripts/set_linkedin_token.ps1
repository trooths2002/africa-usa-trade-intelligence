# PowerShell script to set LinkedIn access token in .env file
# This script helps you properly configure your LinkedIn API credentials

Write-Host "========================================" -ForegroundColor Green
Write-Host "🔐 LINKEDIN ACCESS TOKEN SETUP SCRIPT" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Get the path to the .env file
$envFilePath = Join-Path $PSScriptRoot "..\.env"

Write-Host "Current LinkedIn settings in .env file:" -ForegroundColor Yellow
Get-Content $envFilePath | Where-Object { $_ -like "LINKEDIN_*" -and $_ -notlike "#*" }

Write-Host ""
Write-Host "📋 INSTRUCTIONS:" -ForegroundColor Cyan
Write-Host "1. Generate a token using the LinkedIn Developer Portal:" -ForegroundColor White
Write-Host "   - Go to https://www.linkedin.com/developers/" -ForegroundColor Gray
Write-Host "   - Select your app: 'Free World Trade Africa-USA Trade Intelligence'" -ForegroundColor Gray
Write-Host "   - Go to the 'Auth' tab" -ForegroundColor Gray
Write-Host "   - Scroll to 'OAuth 2.0 tools' section" -ForegroundColor Gray
Write-Host "   - Click 'Token Generator'" -ForegroundColor Gray
Write-Host "   - Select scopes and generate token" -ForegroundColor Gray
Write-Host "2. Copy the generated token to clipboard" -ForegroundColor White
Write-Host ""

# Ask user if they want to update the token
$confirmation = Read-Host "Do you want to update the LinkedIn access token in .env file? (y/n)"

if ($confirmation -eq 'y' -or $confirmation -eq 'Y') {
    $newToken = Read-Host "Enter your LinkedIn access token"
    
    if ($newToken -ne "") {
        # Read the current .env file
        $envContent = Get-Content $envFilePath
        
        # Update the LINKEDIN_ACCESS_TOKEN line
        $updatedContent = $envContent | ForEach-Object {
            if ($_ -like "LINKEDIN_ACCESS_TOKEN=*") {
                "LINKEDIN_ACCESS_TOKEN=$newToken"
            } else {
                $_
            }
        }
        
        # Write back to the .env file
        $updatedContent | Set-Content $envFilePath
        
        Write-Host "✅ LinkedIn access token updated successfully!" -ForegroundColor Green
        Write-Host "You can now test the LinkedIn API integration." -ForegroundColor Yellow
    } else {
        Write-Host "❌ No token entered. Update cancelled." -ForegroundColor Red
    }
} else {
    Write-Host "Update cancelled." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "To test the LinkedIn API integration, run:" -ForegroundColor Cyan
Write-Host "python scripts/test_linkedin_api.py" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Green