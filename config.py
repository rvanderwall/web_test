class Config:
    def __init__(self):
        self.path_to_chrome_driver = "/Users/rvanderwall/opt/chromedriver_mac64/chromedriver"
        self.html_containers = ["div", "span", 'nav']
        self.html_ignore = ['script', 'style', 'noscript', 'br']
        self.include_location = False
        self.prefix = ""
        # self.prefix = "test_"
        self.URL = 'https://www.musicca.com/piano'
