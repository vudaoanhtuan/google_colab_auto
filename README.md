## Keep Google Colab notebook running automatically
-------------------
### Setup
Install Chrome
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb
sudo apt-get install -f
```

Install selenium
```
pip3 install --user selenium
```  
Download Chrome driver at: [link](https://sites.google.com/a/chromium.org/chromedriver/downloads)  
More info: [link](https://selenium-python.readthedocs.io/installation.html)

### Usage
Login your google accout:
```
python3 login.py --driver /path/to/chromedriver
```

Open notebook and create new cell with content `##AUTO##`  
Run `colab.py` and your notebook will be running until you stop this script or running time exceeded limit:
```
python3 colab.py /path/to/cookie_file notebook_url --driver /path/to/chromedriver
```

