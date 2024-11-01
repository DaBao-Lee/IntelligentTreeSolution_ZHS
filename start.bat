@echo off

pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple --user -q
pip install onnxruntime onnx onnxslim opencv-python selenium paddlepaddle paddleocr  fuzzywuzzy -i https://pypi.tuna.tsinghua.edu.cn/simple -q
echo ****************************************************************************
echo The pickles needed have already installed...
echo Start run the script...
echo ****************************************************************************

python main.py -y

pause
exit