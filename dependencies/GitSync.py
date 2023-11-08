import subprocess
import platform

def git_commands():
    if platform.system() == 'Windows':
        batch_script = '''
        @echo off
        git add .
        git commit -m "Git-backed-diary"

        git config --get credential.helper > nul
        if %errorlevel% equ 0 (
            echo Git credentials are already stored.
        ) else (
            set /p store_credentials=Do you want to store your Git credentials? (y/n):
            if "%store_credentials%" == "y" (
                git config --global credential.helper store
            )
        )
        git push
        echo Press any key to continue...
        pause >nul
        '''
        with open("temp_script.bat", "w") as script_file:
            script_file.write(batch_script)
        subprocess.run(['cmd', '/k', 'temp_script.bat'], shell=True)
    else:
        script_content = '''
        #!/bin/bash

        git add .
        git commit -m "Git-backed-diary"

        git config --get credential.helper
        if [ $? -eq 0 ]; then
            echo "Git credentials are already stored."
        else
            read -p "Do you want to store your Git credentials? (y/n): " store_credentials
            if [ "$store_credentials" = "y" ]; then
                git config --global credential.helper store
            fi
        fi
        git push
        echo "Press Enter to continue...(ZSH)"
        read
        '''

        script_filename = "temp_script.sh"
        with open(script_filename, "w") as script_file:
            script_file.write(script_content)

        terminal_emulators = ['xterm', 'gnome-terminal', 'konsole', 'terminator', 'mate-terminal',
                            'rxvt', 'st', 'alacritty', 'tilix', 'guake',
                            'lilyterm', 'cool-retro-term', 'xfce4-terminal', 'terminology', 'kitty',
                            'stjerm', 'sakura', 'tilda', 'yakuake', 'eterm',
                            'hyper', 'roxterm', 'xfce4-terminal', 'liri-terminal', 'pangoterm',
                            'finalterm', 'tilda', 'terminology', 'sakura', 'qterminal',
                            'turbostation', 'guake', 'termite', 'ROXTerm', 'eterm', 
                            'lxterminal', 'mate-terminal', 'PonTTY', 'DDE Terminal', 'PTerm',
                            'Tilda', 'QTerminal', 'pterm', 'kitty', 'mlterm', 'tilix',
                            'Termix', 'Yakuake', 'fbterm', 'terminix', 'Yakuake',
                            'Terminex', 'Cairo', 'Deepin Terminal', 'Tilix', 'Terminix',
                            'Foot', 'Sway Terminal', 'Twin', 'Pantheon Terminal'
                            ]

        for terminal in terminal_emulators:
            try:
                subprocess.run([terminal, '-e', 'bash', script_filename])
                break
            except FileNotFoundError:
                continue
        else:
            print("No supported terminal found to execute the script.")

        subprocess.run(['rm', script_filename])
