from kivymd.app import MDApp
from kivy.core.window import Window
import requests

BaseURL = "https://localhost"
API_Key = "2RQs4LkXj6eQ73c?-YKtPYXg5ce0ERvmVIg4IUMc1q2?DAH/R1IZkxv7sWHNawWb"

class Client(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal" # Try Blue, Purple, Red, etc.
        self.get_countries()

    def get_countries(self):
        try:
            response = requests.get(BaseURL + "/countries", headers = {'API-Key': API_Key}, verify = False)
            if response.status_code == 200:
                text = ""
                for country in response.json():
                    text += "{} (capital: {}, area: {})\n".format(
                        country['name'], country['capital'], country['area'])
                self.root.ids.result_text.text = text
                self.root.ids.status_text.text = "Ready."
            else:
                self.root.ids.status_text.text = "Failed to get countries."
        except:
            self.root.ids.status_text.text = "Failed to connect to the server."

    def add_country(self):
        name = self.root.ids.name_input.text
        capital = self.root.ids.capital_input.text
        area = self.root.ids.area_input.text
        if name and capital and area:
            data = {"name": name, "capital": capital, "area": area}
            try:
                response = requests.post(BaseURL + "/countries", json = data, headers = {'API-Key': API_Key}, verify = False)
                if response.status_code == 201:
                    self.get_countries()
                    self.root.ids.status_text.text = "Country added successfully."
                else: 
                    self.root.ids.status_text.text = "Failed to add the new country."
            except:
                self.root.ids.status_text.text = "Failed to connect to the server."
        else:
            self.root.ids.status_text.text = "Please fill in all fields."

if __name__ == "__main__":
    Window.size = (400, 640)
    Client().run()


