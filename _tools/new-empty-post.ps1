param(
    [Parameter(Mandatory)]
    [string]$Name
    )

$now = Get-Date
$dateString = $now.ToString("yyyy-MM-dd")
$dateTimeString = $now.ToString("yyyy-MM-dd HH:mm:ss zzz")

$cleanName = ((($Name -replace '[^\w\s]', '') -replace '\s+', ' ') -replace ' ', '-').ToLower()
$fileName = "$($dateString)-$($cleanName).md"
$filePath = (Join-Path $PSScriptRoot ".." "_posts" $fileName)

$header = @"
---
layout: post
title:  "$Name"
date:   $dateTimeString
---
"@ 

echo $header > $filePath
Write-Host "Setup new post @ $filePath"