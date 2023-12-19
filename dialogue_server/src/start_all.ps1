# Check if the shared virtual environment exists
if (!(Test-Path -Path ..\.venv)) {
    python -m venv ..\.venv
}

# Sort directories so that 'server' comes first
$directories = $directories | Sort-Object -Property @{Expression = {$_ -eq 'server'}; Descending = $true}, Name

$directories = Get-ChildItem -Directory

foreach ($dir in $directories) {
    if ($dir.Name -eq '__pycache__') {
        continue
    }
    Start-Process powershell -ArgumentList "-NoExit","-Command . ..\.venv\Scripts\activate; cd $dir; pip install -r requirements.txt; python main.py"
}