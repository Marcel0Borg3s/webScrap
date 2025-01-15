$exclude = @("venv", "bankWebDesktop_vsmb.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "bankWebDesktop_vsmb.zip" -Force