# Task 1

This task involved creating a folder `GitHub_Task` on the local system and writing a Python program that prints "Hello World!".  
The folder was then pushed to the GitHub repository using the following Git commands:

cd /d/GitHub_Task
git init
git remote add origin https://github.com/MRM-AIA-TP-27/MRM_ManoharAdimalla.git

echo 'print("Hello World!")' > hello.py
git add hello.py
git commit -m "Task 1: Added Hello World Python program"
git branch -M main
git push -u origin main
