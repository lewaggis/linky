import requests,bs4,time,csv

base = 'https://www.imbernet.net'
urls = [base]
urls_parsed = []
url_responses = {}

def parse(adress):
    target = adress
    
    if (adress[0] == '/'):
        target = base + url
    print("Requesting page...")
    try:
        r = requests.get(target, timeout=20)
        url_responses[target] = r.status_code
    except Exception as exc:
        print("There was a problem: %s" % (exc))
        url_responses[target] = "error"
        
    if (target.find(base) == 0) and (target[-4:] != '.pdf'):
        data = r.text
        soup = bs4.BeautifulSoup(data,features="html.parser")
        for a in soup.select('a[href]'):
            hit = a.get('href')
            print('Found hRef: ' + hit)
            if (hit.find('?') > 1):
                print('-- stripping suffix: ' + hit[hit.find('?'):])
                hit = hit[:hit.find('?')]
                print('-- remaining: ' + hit)
            if (hit.find('#') > 1):
                print('-- stripping anchor:  ' + hit[hit.find('#'):])
                hit = hit[:hit.find('#')]
                print('--remaining:  ' + hit)
            if (hit[0] == '#'):
                print('-- skip: anchor link')
            elif (hit[0:4] == 'java'):
                print('-- skip javascript')
            elif (hit in urls_parsed):
                print('-- skip: aleardy parsed URL')   
            elif (hit in urls):
                print('-- skip: already found URL')
            elif (hit.find('/printpdf/') is not -1):
                print('-- skip: pdf version')
            elif (hit.find('/print/') is not -1):
                print('-- skip: print version:')
            else:
                print("++ adding to queue"  + hit);
                urls.append(hit)
    else:
        print("--link is external or excluded")

while (len(urls) > 0):
    print("\nParsed " + str(len(urls_parsed)) + " pages -  " + str(len(urls)) + " more to go.")
    url = urls.pop()
    print("Discovering " + url)
    time.sleep(0.3)
    parse(url)
    urls_parsed.append(url)

# f = open("dict.txt","w")
# f.write( str(url_responses) )
# f.close()

with open("linky.txt", "w") as textfile:
	writer = csv.writer(textfile, delimiter="\t")
	for key,value in url_responses.items():
		writer.writerow((key,value))
