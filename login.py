import argparse
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

parser = argparse.ArgumentParser()
parser.add_argument('--cookie_file', default='cookie')
parser.add_argument('--driver', default='chromedriver')

if __name__=='__main__':
    args = parser.parse_args()
    driver = webdriver.Chrome(executable_path=args.driver)
    print("Openning Google Colab")
    driver.get("https://colab.research.google.com")
    print("Login with your google account then press enter to continue!")
    input()
    cookie_file_name = args.cookie_file + '.pkl'
    with open(cookie_file_name, 'wb') as f:
        pickle.dump(driver.get_cookies(), f)
    print('Cookies are saved at %s'%cookie_file_name)
    driver.close()