#!/usr/bin/env python
#-*- coding:utf-8 -*-
import doctest
from  os.path import join, dirname, normpath

DATA_PATH = join(dirname(__file__), 'especificao')


from BeautifulSoup import BeautifulSoup
html = BeautifulSoup("<a href='#'><b>teste</b></a>")
from engenhariareversa import DiagramaDeSequencia
a = html.a

with DiagramaDeSequencia('BeautifulSoup find',
    src='exemplos/BeautifulSoup.svg',
    modulos=['BeautifulSoup'],
    ):
        a.find(text='teste')






def filepath(name):
    return normpath(join(DATA_PATH, name))

for spec in ["PicSequencia", "DiagramaDeSequencia", "Contexto", "Filtro", "Sinal"]:
    print doctest.testfile(
        filepath(spec),
        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE + doctest.ELLIPSIS,
        globs=globals())

