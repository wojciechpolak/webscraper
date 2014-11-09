#!/usr/bin/env python
# -*- coding: utf-8 -*-

# webscraper.py -- Simple Web Scraper.
# Copyright (C) 2014 Wojciech Polak.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import time
import getopt
import requests
from lxml import html

try:
    xrange
except NameError:
    xrange = range


def main():
    opts = {
        'url': '',
        'output_dir': '/tmp/',
        'pages': [1, 1],
        'selector': '#posts img:not(.inlineimg)',
        'img_suffix': ('.jpg', '.png',),
    }

    try:
        gopts, args = getopt.getopt(sys.argv[1:], 'o:p:s:',
                                    ['output=',
                                     'pages=',
                                     'img-suffix=',
                                     'selector=',
                                     ])
        for o, arg in gopts:
            if o in ('-o', '--output'):
                opts['output_dir'] = os.path.expanduser(arg)
            elif o in ('-p', '--pages'):
                opts['pages'] = [int(i) for i in arg.split(',')]
            elif o in ('--img-suffix',):
                opts['img_suffix'] = tuple(arg.split(','))
            elif o in ('-s', '--selector'):
                opts['selector'] = arg

        if len(args):
            opts['url'] = args[0]
        else:
            raise getopt.GetoptError('')
    except getopt.GetoptError:
        print("Usage: %s [OPTION...] URL" % sys.argv[0])
        print("%s -- Web Scraper" % sys.argv[0])
        print("""
 Options                       Default values
 -o, --output OUTPUT-DIR       [%(output_dir)s]
 -p, --pages START,STOP        %(pages)s
 -s, --selector CSS-SELECTOR   [%(selector)s]
     --img-suffix SUF1,SUF2    %(img_suffix)s
 
""" % opts)
        sys.exit(1)
    webscrap(opts)


def webscrap(opts):
    try:
        os.makedirs(opts['output_dir'])
    except:
        pass

    for page in xrange(opts['pages'][0], opts['pages'][1] + 1):
        url = opts['url'] + '&page=%d' % page

        response = requests.get(url)
        tree = html.fromstring(response.text)

        i = 0
        for img in tree.cssselect(opts['selector']):
            src = img.get('src').lower()
            if src.endswith(opts['img_suffix']):
                i += 1
                try:
                    name = os.path.basename(img.get('src'))

                    output_img = os.path.abspath(
                        os.path.join(opts['output_dir'],
                                     '%04d-%03d-%s' % (page, i, name)))

                    if os.path.isfile(output_img):
                        print('skipping %s [downloaded]' %
                              os.path.basename(output_img))
                        continue

                    print('downloading %s' % img.get('src'))
                    r = requests.get(img.get('src'), headers={'Referer': url})
                    if r.status_code != 200:
                        print(r.status_code)
                        continue

                    print('saving %s' % os.path.basename(output_img))
                    with open(output_img, 'w') as fp:
                        fp.write(r.content)
                except Exception as e:
                    print(e)
        time.sleep(1)

if __name__ == '__main__':
    main()
