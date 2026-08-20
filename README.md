# CITS5501-3501-Group-Project

Group project repository for CITS5501/CITS3501 Software Testing and Quality Assurance, Semester 2 2026.

When in development ensure environment is as per project specifications:
Ubuntu 22.04 (x86-64 processor) witht he following packages installed:
-python3
-uv
-openjdk-21-jdk

    For those not already in the correct environment:
    1. Download and setup Docker for the appropriate OS and architecture (if not already downloaded)
        - Go to https://www.docker.com/products/docker-desktop/ and download for your OS and Architecture, check Settings for the correct OS and architecture
        - Once downloaded open powershell and the following should run
            docker --version
            docker run hello-world
        (if docker run hello-world does not run install WSL as prompted)

        Restart computer if required

        Install the VSCode extensions:
            Dev Containers by Microsoft
            Container Tools by Microsoft
    2. Open the project in the container
        Use Ctrl+Shift+P (in vscode) and select:
            Dev Containers: Reopen in Container

        The container should load in a workspace called Dev Container

        The current Directory in the terminal attached to VSCode should be under:
            root@xxx:/workspace#

        Once in the container copy paste and run the following into the terminal:
            python3 --version
            uv --version
            javac --version
            git --version
            pwd
            ls
            python3 webscraper/main.py

        The expected output should be:
            Python 3.10.12
            uv 0.12.5 (x86_64-unknown-linux-musl)
            javac 21.0.11
            git version 2.34.1
            /workspace
            README.md  webscraper
            Hello from the web scraper!
            Operating system: Linux
            Architecture: x86_64
