
<#
.SYNOPSIS
Powershell Script for Setup Package Json File

.LINK
    https://www.sidefx.com/docs/houdini/ref/plugins.html

.AUTHOR
    Mandrake0 (Francis Pimenta)
#>


# Getting the Location
$currentLocation = $PSScriptRoot
$UserLocation = "$env:USERPROFILE\Documents\"
$jsonFile = "LVTools.json"
$json = Get-Content $currentLocation\$jsonFile

# Get the Houdini Folder to Write the package JSON File
Set-Location $UserLocation
$HoudiniFolder = Get-Item .\houdini* | Select-Object -Property Name | Out-GridView -Title "Houdini Installation Folder Selection" -PassThru

if (!$HoudiniFolder) {
    Write-Warning "No Houdini Folder Selected, Abort Setup"
    Return 1
}

$Houdini = $HoudiniFolder.Name
$fullpath = $UserLocation + $Houdini

$MSG = @{}
$MSG.Add("Github LV Tools Folder", $currentLocation)
$MSG.Add("Houdini Version", $Houdini)

# Check if Houdini Package Folder Exist
if (!(Test-Path $fullpath\packages)) {
    $MSG.Add("Pagackes Folder Created", "YES")
    New-Item -ItemType Directory -Path $fullpath\packages
} else {
    $MSG.Add("Pagackes Folder Created", "NO")
}

# Create JSON File | it just Overwrites when it exist :-)
Write-Output $json.Replace("/path/to/folder", $currentLocation.Replace("\", "/")) | Out-File -FilePath $fullpath\packages\$jsonFile -Encoding default
$MSG.Add("json File", "$fullpath\packages\$jsonFile")

Write-Output "LV Tools Package Created"
Write-Output $MSG

Read-Host "Press ENTER to Close"