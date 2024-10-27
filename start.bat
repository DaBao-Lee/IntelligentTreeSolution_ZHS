@echo off

pip install onnxruntime onnx onnxslim opencv-python selenium paddlepaddle paddleocr -i https://pypi.tuna.tsinghua.edu.cn/simple
echo ****************************************************************************
echo The pickles needed have already installed...
echo Start run the script...
echo ****************************************************************************

python zhs.py -y

pause
exit