from conn import GroupmeConnection
import requests, json, time

def groupme_recv_thread():
  while True:
    try:
      handshake = {
          "channel": "/meta/handshake",
          "version": "1.0",
          "supportedConnectionTypes": ["long-polling"], # ????
          "id": "1"
          }
      r = requests.get("https://push.groupme.com/faye", params={"message": json.dumps([handshake]), "jsonp": "callback"})
      faye_client_id = json.loads(r.text[4 + len("callback") + 1:-2])[0]["clientId"]
      print("Got faye connection id {}".format(faye_client_id))
      gc = GroupmeConnection(faye_client_id)
      gc.run_forever()
    except Exception as e:
      print(e)
      time.sleep(1)


if __name__ == '__main__':
	# main()
	groupme_recv_thread()

