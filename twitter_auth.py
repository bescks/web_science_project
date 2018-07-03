import twitter

api = twitter.Api(consumer_key='2G1oe9uLv4Dt2ytYo5gTY0VwT',
                  consumer_secret='wv90P5WhcV3j9YYx15xcrkaghpOZO5agzx4yydAC2cJv7b0PR1',
                  access_token_key='734419548254941185-F60GOnT1d5ZRSXTj6uJZlQW1zfWT7Vk',
                  access_token_secret='JLCOG2RpfBzMPfx3QAmWS45QY9Pe6McU1JX0uUn8YMaLJ')

results = api.GetSearch(raw_query="q=como%20&result_type=recent&until=2014-07-19&count=100")
for result in results:
    print(result)
