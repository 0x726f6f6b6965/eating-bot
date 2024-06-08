from openai import OpenAI

class AI:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    def getfoodInfo(self, lat: float, lng: float) -> str:
        text = "I'm hungry and I want to eat something.\
            Please recommend some delicious food within one kilometer near me.\
            I am at latitude {} and longitude {}".format(lat, lng)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": text}],
            temperature=0
            )
        return response.choices[0].message.content