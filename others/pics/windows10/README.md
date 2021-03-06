Windows 10
=============================================

## SW
- python 3.6.0 : https://www.python.org
- git cmd : https://git-for-windows.github.io
- Visual C++ 2015 Build Tools : http://landinghub.visualstudio.com/visual-cpp-build-tools
- florijncoinmnb : https://github.com/chaeplin/florijncoinmnb


### python install
* https://www.python.org

![1](p01.png)

![1](p02.png)

![1](p03.png)

![1](p04.png)


### git install
* https://git-for-windows.github.io

![1](g01.png)

![1](g02.png)

![1](g03.png)

![1](g04.png)

![1](g05.png)

![1](g06.png)

![1](g07.png)

![1](g08.png)

![1](g09.png)

### Visual C++ 2015 Build Tools install
* http://landinghub.visualstudio.com/visual-cpp-build-tools

![1](v01.png)

![1](v02.png)


### florijncoinmnb install
* https://github.com/chaeplin/florijncoinmnb

- open cmd windows
- install virtualenv
```
pip install virtualenv
```
![1](i01.png)

- check git cmd
```
git -v
```
- install florijncoinmnb
```
git clone https://github.com/chaeplin/florijncoinmnb
```
![1](i02.png)


- cd florijncoinmnb and make virtualenv
```
cd florijncoinmnb
virtualenv venv3
```
![1](i03.png)

- activate virtualenv
```
venv3\Scripts\activate.bat
```
![1](i04.png)

- upgrade setuptools
```
pip install --upgrade setuptools
```
![1](i05.png)

- install requirements
```
pip install -r requirements.txt
```
![1](i06.png)

- open florijncoinmnb folder
![1](i07.png)

- copy config.sample.py to config.py and edit
* to use "remote rpc svc by chaeplin" : config.sample.mainnet.remotesvc.py
* to run "your own local/remote florijncoind" : config.sample.mainnet.py

![1](i08.png)
![1](i09.png)

- copy masternode.conf.sample to masternode.conf
![1](i10.png)
![1](i11.png)

- test run
```
cd florijncoinmnb
venv3\Scripts\activate.bat
python bin\florijncoinmnb.py -c
```
![1](i12.png)

- go https://github.com/chaeplin/florijncoinmnb#configuration
* https://github.com/chaeplin/florijncoinmnb#configuration
