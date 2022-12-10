# Face Filtering System
> pattern recognition applications

+ `main.py` 進入點

## Features
+ `.\controller\gui.py` UI 的 controller
+ `.\services\ui.py` 介面
+ `.\services\face_obtain.py` 提取臉部並存進 dataset (人臉偵測與辨識: https://colab.research.google.com/drive/1LOlYpzbhoYSLAtIHMmnjrED55hmrM87_)
+ `.\services\face_compare.py` 比對臉部特徵
    + 需要的 pickle 檔：https://drive.google.com/drive/u/1/folders/1DW4skGaJ0sK6sPp-O1AwAIcJqTX6wE2W

## Reference
+ face dataset: https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/

## 補充
+ 偵測臉部表情 https://github.com/justinshenk/fer?bclid=IwAR23r-_y_isTnQEbi8M1Dx3rNSCBt6AKOR5yY5zFWd3Lu1kzRQwSz7w6BzU
+ https://github.com/Vishwesh4/Face-Feature-Extraction
