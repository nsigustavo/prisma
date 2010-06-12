



Fixture:
    >>> from BeautifulSoup import BeautifulSoup
    >>> html = BeautifulSoup("<a href='#'><b>teste</b></a>")
    >>> from engenhariareversa import DiagramaDeSequencia
    >>> a = html.a

Example:
    >>> with DiagramaDeSequencia('BeautifulSoup find',
    ...     src='exemplos/BeautifulSoup.svg',
    ...     modulos=[BeautifulSoup],
    ...     restringirPrivados=False):
    ...         a.find(text='teste')
    u'teste'

