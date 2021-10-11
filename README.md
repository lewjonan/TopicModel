# TopicModel
Simple implementation of some topic models, such as plsa, lda and so on

## TODO

- [x] plsa
- [ ] lda
- [ ] ...

## Dependencies
- Python 3.6.2
- [numpy](https://github.com/numpy/numpy) 1.19.5
- [jieba](https://github.com/fxsjy/jieba) 0.42.1
- [Scrapy](https://github.com/scrapy/scrapy) 2.5.1
  for scrawl data

All code only runs on Windows. I'm not sure if it can run on other platforms

## Data

I crawled some articles from [bilibili](https://www.bilibili.com/).

stopwords list is from [stopwords](https://github.com/goto456/stopwords)

## Train

You can run as follow

```
python main.py \
data_dir=data/bilibiliarticle \
number_of_topics=100 
max_iters=100
```

## Note

* The code are not well tested, so it may contain bugs.

## Reference

* [http://blog.tomtung.com/2011/10/em-algorithm](http://blog.tomtung.com/2011/10/em-algorithm)
* [http://blog.tomtung.com/2011/10/plsa](http://blog.tomtung.com/2011/10/plsa)
* [https://github.com/hitalex/PLSA/](https://github.com/hitalex/PLSA/)
