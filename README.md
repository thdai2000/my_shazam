# my_shazam
## 1.数据集准备 prepare the dataset
将下载的歌曲转为wav格式，放入```./database/正常/```目录下；将歌曲的加噪版本也转为wav格式，放入```./database/噪声/```目录下；

Convert the original song files to wav, put them in the ```./database/normal/``` directory; convert the noised song files to wav, put them in the ```./database/noise/``` directory;

## 2.生成测试样本 generate the query fragments
运行```python songcutter.py```，运行后会在```./query```目录下看到自动生成的样本

Run ```python songcutter.py```, then the generated queries will be saved in the ```./query``` directory

## 3.生成哈希数据库 generate the hash dataset
运行 ```python datahasher.py```，结束后会在```./middle_results```目录下看到```.npy```格式的哈希数据库，同时在```./plots```目录下可以看到每首歌的频谱图和峰值点

Run ```python datahasher.py```，then the hash dataset will be saved in the ```./middle_results``` directory with the extension ```.npy```; at the same time, you will see the spectrograms in the ```./plots``` directory.

## 4.测试一个样本 test one query
在命令行输入```python query.py -q 样本的路径```
例如：```python query.py -q ./query/噪声/10s/邓紫棋_泡沫_2.wav```
运行后可以在命令行界面看到检索结果的同时，也可以在```./plots```目录下查看该样本的频谱图、峰值点和结果统计柱状图

Run ```python query.py -q [the path of a query]```
eg. ```python query.py -q ./query/noise/10s/邓紫棋_泡沫_2.wav```
The search results will show in the terminal, and the statistics will be saved in the ```./plots```.

## 5.准确率测试 calculate the accuracy
在命令行输入```python evaluate.py --type [噪声/正常] --len [5s/10s/20s] --vote [匹配哈希数/相同时间差]```
例如```python .\evaluate.py --type 噪声 --len 10s --vote 匹配哈希数```
运行后可以在命令行界面查看准确率

Run ```python evaluate.py --type [noise/normal] --len [5s/10s/20s] --vote [aligned hashes/time difference]```
eg. ```python .\evaluate.py --type noise --len 10s --vote aligned hashes```
The accuracy will show in the terminal.
