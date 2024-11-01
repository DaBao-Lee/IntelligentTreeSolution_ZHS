@echo off

color E
echo 正在初始化......
pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple --user -q
pip install onnxruntime onnx onnxslim opencv-python selenium paddlepaddle paddleocr  fuzzywuzzy -i https://pypi.tuna.tsinghua.edu.cn/simple -q

cd data
if exist answers.rar (
 	 tar -xvzf answers.rar
	echo 题库初始化完成
	del answers.rar
) else (
	 echo 
)

cd ../
echo ****************************************************************************
echo The pickles needed have already installed...
echo Start run the script...
echo ****************************************************************************

python main.py -y

pause
exit