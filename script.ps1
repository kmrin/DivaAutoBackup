# Clear garbage
Clear-Host

# Username crap
$username = $env:USERNAME
$profilePath = (Get-ChildItem "C:\Users\" -Filter $username).FullName

# Paths
$documentsPath = [Environment]::GetFolderPath('MyDocuments')
$savePath = $profilePath + '\AppData\Roaming\DIVA'
$segaPath = $profilePath + '\AppData\Roaming\SEGA'
$backPath = $documentsPath + '\DivaBackups'
$steamPath = "C:\Program Files (x86)\Steam\steam.exe"

# Game properties
$gameId = "1761390"
$gameExe = "DivaMegaMix"

# Filename
$datetime = get-date -Format "dd.MM.yy-HHmm"
$filename = "DIVA_" + $datetime + ".7z"

# For script shenanigans
$trackingMessageDisplayed = 0
$sevenZipUrl = "https://www.7-zip.org/"

# Message
Write-Output "  _____  _                            _          ____             _                "
Write-Output " |  __ \(_)                /\        | |        |  _ \           | |               "
Write-Output " | |  | |___   ____ _     /  \  _   _| |_ ___   | |_) | __ _  ___| | ___   _ _ __  "
Write-Output " | |  | | \ \ / / _\` |   / /\ \| | | | __/ _ \  |  _ < / _\` |/ __| |/ / | | | '_ \ "
Write-Output " | |__| | |\ V / (_| |  / ____ \ |_| | || (_) | | |_) | (_| | (__|   <| |_| | |_) |"
Write-Output " |_____/|_| \_/ \__,_| /_/    \_\__,_|\__\___/  |____/ \__,_|\___|_|\_\\__,_| .__/ "
Write-Output "                                                                            | |    "
Write-Output "                                                                            |_|    "
Write-Output "                                                              v1.0.1 by rin "

# Launch DIVA
Write-Host "Starting DIVA..."
Start-Process -FilePath $steamPath -ArgumentList "-applaunch $gameId"

# Try to find DIVA process
Write-Host "Looking for DIVA..."
do{
	$gameProcess = Get-Process | Where-Object {$_.ProcessName -eq $gameExe}
}until($null -ne $gameProcess)

# Track DIVA every second until it closes
do{
    if($trackingMessageDisplayed -eq 0){
        Write-Host "Tracking DIVA..."
        $trackingMessageDisplayed = 1
    }
    Start-Sleep -Milliseconds 1000
}until($gameProcess.HasExited)

# Make sure process is null after DIVA closes
$gameProcess = Get-Process | Where-Object {$_.ProcessName -eq $gameExe}

function exitMessage{
	Write-Output " "
	Write-Output "Thank you for using DivaAutoBackup."
	Start-Sleep -Seconds 5
	exit
}

function doBackup{
	# Anti-dummy
	if((Test-Path $segaPath) -and (Test-Path $savePath)){
		Write-Host "Creating offline save backup..."
	}elseif(Test-Path $segaPath){
		$savePath = $segaPath
		Write-Host "Offline save not found. Backing up default SEGA folder instead."
	}else{
		Write-Host "No saves where found. Exiting."
		exitMessage
	}
	
	# Anti-dummy 2
	if(Test-Path "C:\Program Files\7-Zip"){
		# Do backup
		C:\'Program Files'\7-Zip\7z.exe -bso0 a temp.7z $savePath
		Rename-Item temp.7z $filename
		Move-Item *.7z $backPath
		exitMessage
	}else{
		Write-Host "You don't have 7-Zip. Install it for divaAutoBackup to work."
		Start-Process $sevenZipUrl
		exitMessage
	}
}

# Backup save
if($null -eq $gameProcess){
	if(Test-Path $backPath){
		doBackup
	}else{
		New-Item -ItemType Directory -Path $backPath
		doBackup
	}
}