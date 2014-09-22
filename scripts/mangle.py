# -*- encoding: utf-8 -*-
import re


def mangle(u):
    u = u.strip ('\n')
    u = u.lower()
    u = re.sub(r"[:'&,?]", '', u)
    u = re.sub(ur'[^a-zāūīṃṅñṭḍṇḷ]', '_', u)
    return u
