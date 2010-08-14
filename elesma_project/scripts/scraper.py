"""
Script for parsing cocktail database.
"""

import httplib2
import BeautifulSoup

STARTING_URL = "http://www.iba-world.com/english/cocktails/"

def extract_ingredient(x):
    "Extract the ingredient name, quantity and measurement."
    parts = x.strip().split(" ")
    return { "qty": parts[0], "units": parts[1], "name": " ".join(parts[2:]) }

def stir_cocktail(h, name, group, url):
    "Stir a delightful cocktail. Well, at least download the recipe anyway."
    try:
        resp, content = h.request(url, "GET")
        soup = BeautifulSoup.BeautifulSoup(content)
        body = soup.find('body')
        components = [ x.strip() for x in body.contents if str(x).strip() and str(x) != '<br />' and not hasattr(x, 'name') ]
        if not components:
            components = [ x.strip() for x in body.find('p').contents if str(x).strip() and str(x) != '<br />' and not hasattr(x, 'name') ]

        img = "http://www.iba-world.com/english/cocktails/img/cocktails/%s" % (body.find("img")['src'].split('/')[-1],)
        return { 'name': name,
                 'group': group, 
                 'img': img,
                 'glass': components[0],
                 'instructions': components[-1],
                 'ingredients': [ extract_ingredient(x) for x in components[1:-1] ],
                 }
    except Exception, e:
        print "couldn't stir cocktail: %s in %s\n%s" % (name, group, e,)
        return None

def main(url=STARTING_URL):
    h = httplib2.Http(".cache")
    resp, content = h.request(url, "GET")
    soup = BeautifulSoup.BeautifulSoup(content)
    content_td = soup.find("td", { "class": "content" })
    paragraphs = content_td.findAll('p')
    all_cocktails = []
    while paragraphs:
        try:
            style = paragraphs[0].string.strip()
            cocktails = [ stir_cocktail(h, x.string, style, "%s%s" % (STARTING_URL, x['href'])) for x in  paragraphs[1].findAll("a") ]
            # sometime the ice just doesn't melt right. as bartenders and gentlemen we throw those cocktails away
            all_cocktails = all_cocktails + [ x for x in cocktails if x ]
        except IndexError, e:
            print "Ran out of elements. %s" % (e,)
        except AttributeError, e:
            print "Recieved inappropriate paragraph. %s" % (e,)
        paragraphs = paragraphs[2:]

    return all_cocktails

def main_to_disk(filename='drinks.json', url=STARTING_URL):
    'Write scraped data to disk.'
    data = main(url=url)
    with open(filename, 'w') as fout:
        import django.utils.simplejson as simplejson
        fout.write(simplejson.dumps(data, indent=4))

if __name__ == '__main__':
    main()



