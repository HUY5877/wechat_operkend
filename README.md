环境配置手册
1. cd C:\Users\1\Desktop\SUST\wechat_operkend (此处替换为你的项目url)
2.  conda create -n sust python=3.10  (如果没有环境)
3. conda activate sust
4. python.exe -m pip install --upgrade pip (升级版本)
5. 设置环境变量：
![img.png](img.png)
6. pip install -r requirement.txt 
7. uvicorn app:app --reload (启动后端项目)