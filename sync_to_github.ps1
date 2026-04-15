param (
    [string]$CommitMessage = "chore(sync): master synchronization of project artifacts"
)

Write-Host "Initiating Aegis Sentinel Master Git Synchronization..." -ForegroundColor Cyan

# 1. Stage all modifications (respecting .gitignore rules)
git add .

# 2. Interrogate the Git index for staged changes
$gitStatus = git status --porcelain

if ([string]::IsNullOrWhiteSpace($gitStatus)) {
    Write-Host "[STATUS] Working tree is clean. No uncommitted changes detected. Aborting push." -ForegroundColor Yellow
} else {
    Write-Host "[STATUS] Uncommitted changes detected. Securing state to repository..." -ForegroundColor Cyan
    
    # 3. Commit the changes
    git commit -m $CommitMessage
    
    # 4. Push to remote origin
    Write-Host "[STATUS] Transmitting data to GitHub..." -ForegroundColor Cyan
    git push origin main
    
    Write-Host "[SUCCESS] Master Synchronization Complete. All assets are safely stored on GitHub." -ForegroundColor Green
}