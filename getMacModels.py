import urllib2
import requests as rq
from bs4 import BeautifulSoup
import datetime, json

def get_model_info(model):
	infos = model.find_all('p')

	if len(infos) > 2:
		_deviceName = infos[0].text.strip().replace('\n ', '').replace('\r', '')
		_identifierName = infos[1].text.replace('\n', '').replace('\r', '')[len("Model Identifier:"):].strip()
		#print _deviceName
		#print _identifierName
		return [_identifierName, _deviceName]

	return []

def parseDupInfo(info1, info2, splitStr):
	arr1 = info1.split(splitStr)
	arr2 = info2.split(splitStr)

	if len(arr1) != len(arr2):
		return info2
	else:
		newModelInfo = ""
		for idx in range(len(arr1)):
			if idx > 0:
				newModelInfo += ", "

			if (arr1[idx] == arr2[idx]):
				newModelInfo += arr1[idx].strip()
			else:
				newModelInfo += (arr1[idx].strip() + "/" +arr2[idx].strip())

		return newModelInfo

def parseHtml(dom):
	soup = BeautifulSoup(dom, 'html.parser')
	divs = soup.find_all('div', 'grid2col', 'extra-react-div')
	models = {}

	for d in divs:
		modelInfo = get_model_info(d)
		if len(modelInfo) > 0:
			#print modelInfo
			if modelInfo[0] in models:
				ModelName = modelInfo[1][:modelInfo[1].find('(')]

				ModelInfo1 = modelInfo[1][modelInfo[1].find('(') + 1:modelInfo[1].find(')')]
				ModelInfo2 = models[modelInfo[0]][models[modelInfo[0]].find('(') + 1:models[modelInfo[0]].find(')')]
				splitStr = ','

				if len(ModelInfo1.split(splitStr)) <= 0:
					splitStr = ' '

				models[modelInfo[0]] = ModelName.strip() + " (" + parseDupInfo(ModelInfo1, ModelInfo2, ',') + ")"
			else:
				models[modelInfo[0]] = modelInfo[1]

	return models

def getHtml(url):
	#file = open("ELTA_HTML.htm", "r") 
	#return file.read() 

    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        , "Connection": "keep-alive"
        , "Referer": "http://www.wantu.cn/"
        ,"Accept":"application/json, text/plain, */*"
    }

    req = urllib2.Request(url, headers=header)
    html = urllib2.urlopen(req)
    htmlData = html.read()
    return htmlData

def writeJson(filename, data):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)

def main():
	MacInfoURL = {
		#"iPod touch": "https://support.apple.com/en-us/HT204217",
		#"iPad": "https://support.apple.com/en-us/HT201471",
		#"Apple Watch": "https://support.apple.com/en-us/HT204507",
		#"Apple TV": "https://support.apple.com/en-us/HT200008",
		"MacBook Pro": "https://support.apple.com/en-us/HT201300",
		"MacBook Air": "https://support.apple.com/en-us/HT201862",
		"MacBook": "https://support.apple.com/en-us/HT201608",
		"iMac": "https://support.apple.com/en-us/HT201634",
		"Mac mini": "https://support.apple.com/en-us/HT201894",
		"Mac Pro": "https://support.apple.com/en-us/HT202888"
	}

	for attr, value in MacInfoURL.iteritems():
		#print attr, value
		html_doc = getHtml(value)
		models = parseHtml(html_doc)
		print models
		writeJson("json/" + attr.replace(' ', '_') + ".json", models)

	#url = "http://support.apple.com/kb/ht4132" 
	#response = getHtml(url)
	#html_doc = getHtml(url)

	#get_schedule(html_doc)

if __name__ == "__main__":
    main()
