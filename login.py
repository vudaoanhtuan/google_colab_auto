import getpass
import argparse
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from cipher import encrypt

parser = argparse.ArgumentParser()
parser.add_argument('--cookie_file', default='cookie')
parser.add_argument('--driver', default='chromedriver')

def get_password():
    pw = None
    pw_cf = None 
    while True:
        pw = getpass.getpass(prompt='Enter password: ')
        pw_cf = getpass.getpass(prompt='Verify password: ')
        if pw==pw_cf:
            break
        else:
            print("Verify failure. Try again!")
    return pw


if __name__=='__main__':
    args = parser.parse_args()

    driver = webdriver.Chrome(executable_path=args.driver)

    print("Openning Google Colab")
    driver.get("https://colab.research.google.com")
    print("Login with your google account then press enter to continue!")
    input()

    password = get_password()
    cookie = pickle.dumps(driver.get_cookies())
    data = encrypt(cookie, password)
    cookie_file_name = args.cookie_file + '.pkl'
    with open(cookie_file_name, 'wb') as f:
        f.write(data)
    print('Cookies are saved at %s'%cookie_file_name)
    driver.close()