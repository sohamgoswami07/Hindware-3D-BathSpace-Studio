$files = Get-ChildItem -Recurse -File -Path "assets", "models"
$counter = 0
$totalFiles = $files.Count
Write-Host "Found $totalFiles files to process."

foreach ($file in $files) {
    if ($file.FullName -match "node_modules") { continue }
    
    $status = git status --porcelain $file.FullName
    if ($status) {
        git add $file.FullName
        $counter++
        
        git commit -m "Add asset $counter of $totalFiles: $($file.Name)"
        Write-Host "Committing file $counter of $totalFiles: $($file.Name)..."
        
        $retryCount = 0
        do {
            git push
            if ($LASTEXITCODE -eq 0) { 
                Write-Host "Pushed file $counter successfully."
                break 
            }
            $retryCount++
            if ($retryCount -gt 10) {
                Write-Host "Max retries reached for file $counter. Exiting."
                exit 1
            }
            Write-Host "Push failed, retrying in 10s..."
            Start-Sleep -Seconds 10
        } while ($true)
    }
}
