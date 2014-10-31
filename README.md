Simple Web Scraper
==================

This is a simple web scraper written for a photo extracting.

    Usage: ./webscraper.py [OPTION...] URL
    ./webscraper.py -- Web Scraper

    Options                       Default values
    -o, --output OUTPUT-DIR       [/tmp/]
    -p, --pages START,STOP        [1, 1]
    -s, --selector CSS-SELECTOR   [#posts img:not(.inlineimg)]
        --img-suffix SUF1,SUF2    ('.jpg', '.png')

Example Usage
-------------

Extract photos from SkyscraperCity forum:

    ./webscraper.py -p 100,122 -o ~/sky-lodz-centrum/ http://www.skyscrapercity.com/showthread.php?t=1659349
