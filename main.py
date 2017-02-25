#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------
# | Author:   钱磊(Qian Lei)
# | Email:    qianlei90@gmail.com
# | Date:     2017-02-23 18:45:59
# | Version:  1.0
# --------------------------------
#

from utils.tasks import async_find_item

if __name__ == "__main__":
    search_kw = 'kids canopy'
    target = 'Octorose ® Butterfly Bed Canopy Mosquito NET Crib Twin Full Queen King (purple)'
    num = 8

    for i in range(num):
        async_find_item.delay(search_kw=search_kw, target=target)
