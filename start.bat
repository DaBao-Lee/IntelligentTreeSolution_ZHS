@echo off

color E
echo ****************************************************************************
echo Initializing...
pip install onnxruntime onnx onnxslim opencv-python selenium paddlepaddle paddleocr  fuzzywuzzy -i https://pypi.tuna.tsinghua.edu.cn/simple -q

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

python main.py  -y

pause
exit