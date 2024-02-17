# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted; iwr -useb https://gitlab.com/krafi/git-backed-diary/-/raw/main/win_setup.ps1 | iex

#  pip3 install  noisereduce torch  --upgrade --force-reinstall

$retryCount = 0
$maxRetries = 3

if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
Write-Host "This program will download and install choco, ffmpeg, Python 3.11.5, Git 2.43.0, certain pip packages, and clone the 'git-backed-diary' project." -ForegroundColor Yellow
    $confirmation = Read-Host "Do you want to continue? (Y/N)"

    if ($confirmation -ne "Y" -and $confirmation -ne "y") {
        Write-Host "Operation canceled by user." -ForegroundColor Green
        Exit
    }
    while ($true){
        Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted;
        Write-Output "Winutil needs to be run as Administrator. Attempting to relaunch."
        $url = "https://gitlab.com/krafi/git-backed-diary/-/raw/main/win_setup.ps1"
        # $url = "https://gitlab.com/krafi/git-backed-diary/-/raw/main/win_setup.ps1"
        $outputPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop\win_setup.ps1")

        $process = Start-Process -Verb runas -FilePath powershell.exe -ArgumentList "iwr -useb $url -OutFile $outputPath; iex $outputPath" -PassThru
        
        $process.WaitForExit()
        if ($process.ExitCode -ne 1) {
            Write-Output($process.ExitCode)
            $process = Start-Process -FilePath powershell.exe -ArgumentList "pip3 install  noisereduce --upgrade --force-reinstall" -PassThru
            $process.WaitForExit()
            Write-Host "Now you will find your git-backed-diary at desktop" -ForegroundColor Green
            Read-Host "Program was successful , Press any enter to exit the program" -ForegroundColor Green
            Exit
        }
        $retryCount++
        if ($retryCount -ge $maxRetries) {
            Read-Host "Maximum retry limit reached. Exiting script."
            Exit
            }
    }

}

        
#  https://gitlab.com/krafi/code-git/-/raw/master/story_web/exitzero.ps1   # exit 1
#  https://gitlab.com/krafi/code-git/-/raw/master/story_web/exitzeroreal.ps1   # "exit 0"


$ErrorActionPreference = "Stop"
#$host.Exit()


Write-Host "If you see any error/issue run this program or script again" -ForegroundColor Green -BackgroundColor Black
Write-Host "python-3.11.5 is about 25Mb downloading 25Mb" -ForegroundColor Green -BackgroundColor Black
Start-Sleep -Seconds 5

# Define variables
$pythonInstallerUrl = "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe"
$installPath = "C:\Python3.11.5"
$gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"

# Set the desktop path
$desktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")

# Download Python installer to desktop
Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile "$desktopPath\python-installer.exe"

# Install Python silently
Start-Process -Wait -FilePath "$desktopPath\python-installer.exe" -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0"

# Remove the Python installer from the desktop
Remove-Item "$desktopPath\python-installer.exe"
# Display installed Python version
Write-Host "Python 3.11.5 has been installed to $installPath" -ForegroundColor Green -BackgroundColor Black




Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco install ffmpeg-full --force -y




Write-Host "Git is about 60mb...." -ForegroundColor Green -BackgroundColor Black

Start-Sleep -Seconds 3
# Define variables
$pythonInstallerUrl = "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe"
$installPath = "C:\Python3.11.5"
$gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"

# Set the desktop path
$desktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")

# Download Python installer to desktop
Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile "$desktopPath\python-installer.exe"

# Install Python silently
Start-Process -Wait -FilePath "$desktopPath\python-installer.exe" -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0"

# Remove the Python installer from the desktop
Remove-Item "$desktopPath\python-installer.exe"

# Download Git installer to desktop
Invoke-WebRequest -Uri $gitInstallerUrl -OutFile "$desktopPath\git-installer.exe"

# Install Git silently
Start-Process -Wait -FilePath "$desktopPath\git-installer.exe" -ArgumentList "/SILENT"

# Remove the Git installer from the desktop
Remove-Item "$desktopPath\git-installer.exe"



# Check if git command is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Error: 'git' is not recognized. Please ensure Git is installed and added to the system PATH." -ForegroundColor Red
    $host.Exit()

}

# Display installed Git version
$gitVersion = git --version

Write-Host "Git $gitVersion has been installed." -ForegroundColor Green -BackgroundColor Black

# Update Git
git update-git-for-windows

# Display updated Git version
$updatedGitVersion = git --version

Write-Host "Git has been updated to $updatedGitVersion."

if (Get-Command pip -ErrorAction SilentlyContinue) {

    $pythonPackages = @(
        "Crypto==1.4.1",
        "cryptography==37.0.2",
        "passlib==1.7.4",
        "bcrypt==4.0.1",
        "PySide6==6.6.0",
        "pycryptodome==3.18.0",
        "markdown2==2.4.9",
        "pillow==10.1.0",
        "pyaudio==0.2.14",
        "pydub==0.25.1",
        "noisereduce==3.0.0",
        "torch==2.1.1"
    )

    foreach ($package in $pythonPackages) {
        pip install $package
    }

    Write-Host "Python packages have been successfully installed."
} else {

    Write-Host "Error: 'pip' is not recognized. Please ensure Python is installed and added to the system PATH." -ForegroundColor Red
    $host.Exit()
}

Start-Sleep -Seconds 3

# Open GitLab project in the default browser
Write-Host "Great, now you need to fork the project from GitLab."  -ForegroundColor Green -BackgroundColor Black Read-Host
Start-Sleep -Seconds 5

Write-Host "If you are running this script for the first time, it's normal to see an error like 'pip : The term 'pip' is not recognized.' You need to run this program again. You can close this program here." -ForegroundColor Red -BackgroundColor White


$choice = Read-Host "Do you have a GitLab account? (Y/N)"

if ($choice -eq "Y" -or $choice -eq "y") {
    Write-Host "Great, Let's fork the project and copy "Clone with HTTPS" link"  -ForegroundColor Green -BackgroundColor Black Read-Host
    Write-Host "Then, copy "Clone with HTTPS" link"  -ForegroundColor Green -BackgroundColor Black Read-Host
    Write-Host "Then, paste link Here"  -ForegroundColor Green -BackgroundColor Black Read-Host
                  
    Start-Sleep -Seconds 7
    $gitLabProjectUrl = "https://gitlab.com/krafi/git-backed-diary/-/forks/new"
    Start-Process $gitLabProjectUrl
}

else {
    $signUpUrl = "https://gitlab.com/users/sign_up"
    Start-Process $signUpUrl

    do {
        $profileComplete = Read-Host "Has your GitLab profile creation been completed? (Y/N)"
        
        if ($profileComplete -eq "Y" -or $profileComplete -eq "y") {
            $gitLabProjectUrl = "https://gitlab.com/krafi/git-backed-diary/-/forks/new"
            Start-Process $gitLabProjectUrl
        }
        else {
            Write-Host "Please complete your GitLab profile creation."
            Start-Sleep -Seconds 3
            $signUpUrl = "https://gitlab.com/users/sign_up"
            Start-Process $signUpUrl
        }
    } while (!($profileComplete -eq "Y" -or $profileComplete -eq "y"))
}

$desktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")

do {
    Write-Host "Make sure you've copied the Git clone link"
    $gitLink = Read-Host "Enter Git HTTPS link | Right-click to paste link"

    $repoName = ($gitLink -split '/').TrimEnd('.git') | Select-Object -Last 1
    $repoPath = Join-Path -Path $desktopPath -ChildPath $repoName

    $gitCloneCommand = "git clone --depth 1 $gitLink `"$repoPath`""
    $cloneResult = Invoke-Expression $gitCloneCommand

    if ($LASTEXITCODE -ne 0 -or $cloneResult -like '*fatal*') {
        Write-Host "Failed to clone the repository. Please check the Git link and try again."
        Write-Host "git-backed-diary already exists in your Desktop, You need to remove that folder."
    }
    else {
        Write-Host "Repository cloned successfully at $repoPath."
    }
} while ($LASTEXITCODE -ne 0 -or $cloneResult -like '*fatal*')

Write-Host "Now you will find your git-backed-diary at desktop" -ForegroundColor Green
Read-Host "Program was successful , Press any enter to exit the program" -ForegroundColor Green
exit 0

# Get-ExecutionPolicy -List
# Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy Unrestricted
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted

