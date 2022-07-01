from selenium import webdriver
from flask import Flask
from selenium.webdriver.chrome.options import Options
from waitress import serve
app = Flask(__name__)


@app.route('/')
def hello():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.lemonde.fr")
    element_text = driver.page_source
    driver.quit()
    return element_text

if __name__ == '__main__':
    serve(app,host = '0.0.0.0',port = 5000)
