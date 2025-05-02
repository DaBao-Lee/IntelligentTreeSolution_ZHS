@echo off

color E
echo ****************************************************************************
echo Initializing...
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple -q

cd data
if exist answers.rar (
 	 tar -xvzf answers.rar
	echo Initialization over...
	del answers.rar
) else (
	echo Initialization over..
)

cd ../
echo ****************************************************************************
echo The pickles needed have already installed...
echo Start run the script...
echo ****************************************************************************
cd ../
if exist vscode (
	cd IntelligentTreeSolution_ZHS-main
	python3.9 main.py  -y --headless
) else (
	cd IntelligentTreeSolution_ZHS-main
	python main.py  -y --headless
)

pause
exit