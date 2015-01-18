pyrez
======

**pyrez** is the first [Songbee][] client. It features a quite nice CLI and... that's it, I think.

[Songbee]: https://songbee.net/

Usage
------

1. Spawn a development repo server (`cd test_server; python -m SimpleHTTPServer 9876`)
2. In separate terminal window, run `pyrez repo add "http://127.0.0.1:9876/index.json"`
3. `pyrez update`
4. `pyrez lookup --title Alive`

Structure
----------

Songbee uses *repositories* to manage music tracks. This is quite similar to how software repositories, like APT, work. The repository channel is a JSON file like this one:

```
{
  "v": 1,
  "id": "net.songbee.repo.white.alpha",
  "maintainer": "Ale <ale@incrowd.ws>",
  "tracks": [{
    "id": "mindvortexalive",
    "artist": "Mind Vortex",
    "title": "Alive",
    "uri": "http://127.0.0.1:9876/blob/mwa.flac"
  }]
}
```

(the schema is yet to discuss)

pyrez can manage a local database of tracks and update it from a couple of servers. It can also look up a track, using the `lookup` command. The actual music streaming is yet to be done, but this would probably be easy.

This actually means Songbee is a federation, yay!

Roadmap
--------

- [ ] HTTP streaming
- [ ] BitTorrent streaming
- [ ] Move on to a GUI version..?