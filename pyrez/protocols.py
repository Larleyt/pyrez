import requests

class Protocol:
  # interface?
  pass

class HTTPv1(Protocol):
  def __init__(self, uri):
    self.uri = uri

  def get_meta(self):
    r = requests.get(self.uri)
    return r.json()

  def get_tracks(self):
    r = requests.get(self.uri)
    return r.json()['tracks']

# A little roadmap:
# - git / https+git
# - tor+*
# - i2p+* (via i2pd)
# - tribler
# - more p2p stuff

def make_protocol(uri):
  pr = uri.split(":")[0]
  if pr in ["http", "https"]:
    return HTTPv1(uri)
  else:
    raise Exception("NIY")