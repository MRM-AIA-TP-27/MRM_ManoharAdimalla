# Task 4 and Task 5

## Task 4
A new branch named **Temp** was created, and the file `Task_3.md` was added to document Task 3.  
The following commands were used:

git checkout -b Temp
cat > Task_3.md << 'EOF'

Task 3

...
EOF
git add Task_3.md
git commit -m "Task 4: Added Task_3.md on Temp branch"
git push -u origin Temp


---

## Task 5
The **Temp** branch was merged into the **main** branch and pushed to GitHub.

Commands used:

git checkout main
git merge Temp
git push origin main
