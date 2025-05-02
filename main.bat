@ echo off
color c
cd /d C:\Users\Public

if exist IntelligentTreeSolution_ZHS-main (
	cd /d C:\Users\Public\IntelligentTreeSolution_ZHS-main
	start start.bat
) else (
 curl -o main.zip https://codeload.github.com/DaBao-Lee/IntelligentTreeSolution_ZHS/zip/refs/heads/main
 tar -xvzf main.zip
cd /d C:\Users\Public\IntelligentTreeSolution_ZHS-main
start start.bat
cd ../
del main.zip
)





