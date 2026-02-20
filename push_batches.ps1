$files = Get-ChildItem -Recurse -File -Path "assets", "models"
$batchSize = 25
$counter = 0
$totalFiles = $files.Count
Write-Host "Found $totalFiles files to process."

foreach ($file in $files) {
    if ($file.FullName -match "node_modules") { continue }
    
    $status = git status --porcelain $file.FullName
    if ($status) {
        git add $file.FullName
        $counter++
        
        if ($counter % $batchSize -eq 0) {
            $batchNum = [math]::Ceiling($counter / $batchSize)
            git commit -m "Add asset batch $batchNum"
            Write-Host "Committing batch $batchNum ($counter / $totalFiles)..."
            
            $retryCount = 0
            do {
                git push
                if ($LASTEXITCODE -eq 0) { 
                    Write-Host "Pushed batch $batchNum successfully."
                    break 
                }
                $retryCount++
                if ($retryCount -gt 5) {
                    Write-Host "Max retries reached for batch $batchNum. Exiting."
                    exit 1
                }
                Write-Host "Push failed, retrying in 5s..."
                Start-Sleep -Seconds 5
            } while ($true)
        }
    }
}

# Final push
git commit -m "Add remaining assets"
do {
    git push
    if ($LASTEXITCODE -eq 0) { break }
    Start-Sleep -Seconds 5
} while ($true)
