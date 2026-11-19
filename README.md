# news-image-20261118

[![make.fun ·
news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

[![rank](https://make.fun/badge/news-image-20261118/vnazt/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

[![reward](https://make.fun/badge/news-image-20261118/vnazt/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Wednesday 18 November 2026: 27 stories, 5 continents — one front page. The hero story is Voyager 1 reaching one light-day from Earth, 16.1 billion miles out, its signal now taking 24 hours to come home — drawn as the day's defining picture. Around it, the front page carries the rest of the day: APEC opening in Shenzhen, where Xi Jinping urges free and open trade and defends the WTO; Xi meeting Putin in Shenzhen ahead of the first-ever trilateral with Trump; Quad leaders meeting in Manila, their first leader-level gathering in more than two years; Mary Peltola winning the Alaska Senate race for the Democrats, 56–44; the United States losing its measles-free status, with PAHO counting 5,412 cases and 10 deaths in 2026; and Cyclone Akvan turning severe in the Bay of Bengal — with a ticker along the bottom holding four more stories that would not fit the page: the Gulf flashpoint, a Kerch Bridge span falling, Ebola topping 11,000 cases in DR Congo, and a Siberia crash killing 19.

The deliverable is `entry.png` (1024x1024). `main.py` is the entry program: it validates the image against the bounty limits (PNG signature, every chunk with its checksum through to IEND, IHDR width and height at most 1024, at most 1 MiB) and copies it unchanged into the output directory, confirming the byte count as it goes. Standard library only, no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ws8tc7yd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
