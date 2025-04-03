#!/bin/bash

# Initialize Git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit of Attendance Calculator"

# Instructions for pushing to GitHub
echo "Repository initialized successfully!"
echo ""
echo "To push to GitHub, run the following commands:"
echo "1. Create a new repository on GitHub (don't initialize with README, .gitignore, or license)"
echo "2. Run the following commands:"
echo "   git remote add origin https://github.com/yourusername/attendance-calculator.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "Replace 'yourusername' with your actual GitHub username."
