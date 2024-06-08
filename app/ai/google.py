import google.generativeai as genai

class AI:
    def __init__(self, key):
        genai.configure(api_key=key)
        self.ai =  genai.GenerativeModel('gemini-1.5-flash')

    def generate(self, prompt):
        return self.ai.generate_content(prompt)
    
    def getfoodInfo(self, lat: float, lng: float) -> str:
        text = "I'm hungry and I want to eat something. \
            Please recommend some delicious food within one kilometer near me. \
            I am at latitude {} and longitude {}".format(lat, lng)
        resp = self.generate(text)
        return resp.text