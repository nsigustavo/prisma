#!/usr/bin/env python
#-*- coding:utf-8 -*-

from BeautifulSoup import BeautifulSoup
html = BeautifulSoup("<a href='#'><b>teste</b></a>")
from engenhariareversa import DiagramaDeSequencia
a = html.a


with DiagramaDeSequencia(
    'BeautifulSoup find',
    src='exemplos/BeautifulSoup.svg',
    modulos=['BeautifulSoup'],):
        a.find(text='teste')

