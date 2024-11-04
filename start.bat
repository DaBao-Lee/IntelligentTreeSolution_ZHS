@echo off

color E
echo ****************************************************************************
echo Initializing...
pip install onnxruntime onnx onnxslim opencv-python selenium paddlepaddle paddleocr fuzzywuzzy python-levenshtein -i https://pypi.tuna.tsinghua.edu.cn/simple -q
pip install ultralytics ddddocr pillow -i https://pypi.tuna.tsinghua.edu.cn/simple -q

cd data
if exist answers.rar (
 	 tar -xvzf answers.rar
	echo Initialization over...
	del answers.rar
) else (
	echo Initialization over...
)

cd ../
echo ****************************************************************************
echo The pickles needed have already installed...
echo Start run the script...
echo ****************************************************************************
cd ../ 

if exist vscode (
	cd IntelligentTreeSolution_ZHS-main
	python3.9 main.py  -y
) else (
	cd IntelligentTreeSolution_ZHS-main
	python main.py  -y
)

pause
exit