class Config:
    def __init__(self):
        self.path_to_chrome_driver = "/Users/rvanderwall/opt/chromedriver_mac64/chromedriver"

        self.html_containers = ["div", "span", 'nav']
        self.html_ignore = ['script', 'style', 'noscript', 'br', 'svg']

        self.include_location = False
        self.prefix = "MP_"
        self.URL = 'https://www.musicca.com/piano'
        self.prefix = "CRU_"
        self.URL = 'http://localhost:3000/'

        self.prefix = "CRU_S_"
        self.URL = 'http://localhost:3000/search'
