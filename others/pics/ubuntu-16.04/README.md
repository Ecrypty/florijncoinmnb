ubuntu-16.04 
=============================================

### 1) open Terminal
![1](./u01.png)


### 2) open florijncoinmnb page
![1](./u02.png)
![1](./u03.png)


### 3) download installation script
```
wget https://raw.githubusercontent.com/chaeplin/florijncoinmnb/master/others/linux/ubuntu-16-04.sh
```
![1](./u04.png)

### 4) excute ubuntu-16-04.sh
```
sh ./ubuntu-16-04.sh
```
![1](./u05.png)

### 5) when finished following screen will appear

![1](./u06.png)


### 6) open folder ~/florijncoinmnb/florijncoinlib and duoble click config.py

gedit will open it

edit redd box and save it

https://github.com/chaeplin/florijncoinmnb/tree/master/others/pics/trezor has example
![1](./u07.png)



### 6) open folder ~florijncoinmnb/mnconf and rename masternode.conf.sample to masternode.conf

duoble click masternode.conf, gedit will open it

edit redd box and save it

![1](./u08.png)

### 7) use following command to start
```
cd ~/florijncoinmnb
. venv3/bin/activate
python bin/florijncoinmnb.py


python bin/florijncoinmnb.py -c


python bin/florijncoinmnb.py -b
```


![1](./u09.png)

