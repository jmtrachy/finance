import httplib
from xml.dom.minidom import parse, parseString

if __name__ == "__main__":
    h1 = httplib.HTTPSConnection('www.google.com')
    h1.request("GET", '/finance?q=NASDAQ%3ASCTY')
    response = h1.getresponse()
    data = response.read()

    div_index = data.index('<div id="sharebox-data"')
    temp_string = data[div_index:]

    div_close_index = temp_string.index('</div>')
    xml_snippet = temp_string[:div_close_index + 6]
    containing_div = xml_snippet.index('">')

    xml_snippet = xml_snippet[:containing_div + 1] + ' ' + xml_snippet[containing_div + 1:]
    xml_snippet = xml_snippet.replace('&', '&amp;')
    xml_snippet = xml_snippet.replace('">', '"/>')

    dom = parseString(xml_snippet)
    children = dom.getElementsByTagName('meta')

    for child in children:
        field_name = child.attributes['itemprop'].value
        field_value = child.attributes['content'].value
        print(field_name + ' = ' + field_value)