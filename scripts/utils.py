# -*- coding: utf-8 -*-
import re

def mangle_title(title):
    title = title.lower()
    title = re.sub(ur"[^a-zāīūṃṅñṭḍṇḷ\s]", "", title)
    title = re.sub(r"\s+", "-", title)
    return title
