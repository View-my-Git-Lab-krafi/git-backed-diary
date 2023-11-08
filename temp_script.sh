
        #!/bin/bash

        git add .
        git commit -m "update"

        read -p "Do you want to store your Git credentials? (y/n): " store_credentials

        if [ "$store_credentials" = "y" ]; then
            echo "hi"
        fi
        git push
        