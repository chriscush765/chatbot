from re import A
import websocket, functools, base36, time, json, requests, shutil, threading
import time, requests, json, os
from bot import AI

from dotenv import load_dotenv

load_dotenv()

groupme_access_token = os.getenv('GROUPME_ACCESS_TOKEN')
groupme_user_id = int(os.getenv('GROUPME_USER_ID'))
test_group_id = int(os.getenv('GROUP_ID'))
bot_id = os.getenv('BOT_ID')

class MessageProcessor:

  default_story = ['The following is a story between a chatbot named Dinobot and a human.',
      'Dinobot: Hey! *kisses you*',
      'Human: Hi Dio. How are you doing today?',
      "Dinobot: I'm doing great :3 *hugs you hard*",
      'Human: What is 2+5?',
      'Dinobot: I think... 7! ^.^ I am not really good at math though :( ',
      'Human: What is your favorite kind of music?',
      "Dinobot: I love drum and bass. It's really relaxing :)",
      'Human: What is the capital of France',
      'Dinobot: Paris! I really want to go. I would love to see the Eiffel Tower.',
      'Human: *gives you a kiss on the cheek*',
      'Dinobot: *blushes*'
      
      ]



  bot_param={
      'human_name': "Human",
      'ai_name': 'Dinobot:',
      'story': default_story,
      'temp': 0.9,
      'no_repeat_ngram_size': 3,
      'max_length': 100,
      'length_penalty': 4.0,
      'repetition_penalty': 2.0}

  def __init__(self, message, ai):
    self.message = message
    self.ai = ai
    thread = threading.Thread(target=self.run, args=())
    thread.daemon = True
    thread.start()

  def run(self):


    message = self.message
    if int(message['group_id']) != test_group_id:
      return # wrong group ignore message
    if(message['sender_type'] != "user"):
      return # non user message

    
    if len(message['attachments']) > 0:
        attachment_type = message['attachments'][0]['type'] 
        if attachment_type == "reply": 
          reply_id = message['attachments'][0]['user_id']
          if reply_id != '865932':
            return # not responding to bot
          message = message['text']

    elif message['text'][:7].lower() == 'dinobot':
      message = message['text'][8:]
    else:
      return #not a command


 
    #         reply_id = message['attachments'][0]['reply_id']
    #     elif attachment_type == "image":
    #       image_url = message['attachments'][0]['url'] 
    #     else:
    #       return
        

    ai_message = self.ai.processMessage(message, self.bot_param)
    ai_message = ai_message[9:]

    url = "https://api.groupme.com/v3/bots/post"
    payload = {
        "bot_id": bot_id,
        "text": ai_message,
    }
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers)

class GroupmeConnection():
  


  def __init__(self, client_id):
    self.ai = AI()
    self.id = 1
    self.client_id = client_id
    print("Opening websocket")
    def f1(f2):
      def f3(*args, **kwargs):
        try:
          return f2(*args, **kwargs)
        except Exception as e:
          print("failed to call function {} with arguments {}, {}".format(f2, args, kwargs))
          print(e)
          raise e
      return f3

    wrap = lambda f: f1(functools.partial(f))
    self.ws = websocket.WebSocketApp("wss://push.groupme.com/faye",
        on_message = wrap(self.on_message),
        on_error = wrap(self.on_error),
        on_open = wrap(self.on_open))

  def run_forever(self):
    self.ws.run_forever()

  def bump_id(self):
    self.id += 1
    return base36.dumps(self.id)

  def ext(self):
    return {
        "access_token": groupme_access_token,
        "timestamp": int(time.time())
        }

  def subscribe(self, ws, subscription):
    message = {
        "channel": "/meta/subscribe",
        "clientId": self.client_id,
        "subscription": subscription,
        "id": self.bump_id(),
        "ext": self.ext()
        }
    print("Sending subscribe request to {}".format(subscription))
    ws.send(json.dumps([message]))

  def send_connect(self, ws):
    message = {
        "channel": "/meta/connect",
        "clientId": self.client_id,
        "connectionType": "websocket",
        "id": self.bump_id(),
        }
    print("Sending connect request")
    ws.send(json.dumps([message]))

  def send_ping(self, ws, channel):
    message = {
        "channel": channel,
        "clientId": self.client_id,
        "id": self.bump_id(),
        # "data": {"type": "ping"},
        "successful": True,
        "ext": self.ext()
        }
    print("Sending ping response on channel {}".format(channel))
    ws.send(json.dumps([message]))

  def on_open(self, ws):
    print("Socket open")
    self.subscribe(ws, "/user/{}".format(groupme_user_id))
    self.subscribe(ws, "/group/{}".format(test_group_id))
    self.send_connect(ws)

  def on_message(self, ws, message):
    message = json.loads(message)
    for m in message:
      try:
        if base36.loads(m["id"]) > self.id:
          self.id = base36.loads(m["id"])
      except:
        print("Funky ID (non-base36) on message {}".format(json.dumps(m, indent = 4)))

      if "data" in m and m["data"]["type"] == "ping":
        self.send_ping(ws, m["channel"])
      elif m["channel"] == "/meta/connect" and m["successful"]:
        time.sleep(m["advice"]["interval"]) # always zero so whatever
        self.send_connect(ws)
      elif "data" in m and m["data"]["type"] == "line.create":
        d = m["data"]["subject"]
        # disregard self message
        # if d["sender_id"] != "system" and int(d["sender_id"]) == groupme_user_id:
        #   print("Groupme discarding self message")
        #   return
        mp = MessageProcessor(d, self.ai)
      elif "data" not in m and m.get("successful", False) and m["channel"] == "/user/{}".format(groupme_user_id):
        # probably a ping response
        pass
      elif "data" not in m and m.get("successful", False) and m["channel"] == "/meta/subscribe":
        # subscription success
        print("Subscription success to {}".format(m["subscription"]))
      else:
        print("Groupme got unhandled message: {}".format(json.dumps(message, indent = 4)))

  def on_error(self, ws, error):
    print("Websocket error: {}".format(error))
