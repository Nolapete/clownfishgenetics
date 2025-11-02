$filePath = "d:\djangoRefactor\clownfishRefactor\crossTesting\pyUpdatedto3\phenotype.py"

# Process the file line by line
Get-Content -Path $filePath | ForEach-Object {
    if ($_ -notmatch '^parent' -and $_ -notmatch [regex]::Escape("' '.join")) {
        if ($_ -match "fmtIt\('([^']*)'\)" -or $_ -match 'fmtIt\("([^"]*)"\)') {
            $Matches[1]
        }
    }
}
