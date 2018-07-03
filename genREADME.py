import datetime, json, os

def writeFile(filename, data):
	with open(filename, 'a') as outfile:
		outfile.write(data.encode('utf-8'))

def readJson(filename):
	with open(filename) as f:
		data = json.load(f)
		return data

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

	readmeFileName = "README.md"

	os.remove(readmeFileName)

	MDData = "# AppleDeviceWithIdentifierName\n\
Apple device's name map model Identifier (Mac)\n\
\n\
"
	writeFile(readmeFileName, MDData)

	for attr, value in MacInfoURL.iteritems():
		print attr, value
		jsonFileName = "json/" + attr.replace(' ', '_') + ".json"

		writeFile(readmeFileName, "\n## [" + attr + "](" +jsonFileName+ ")\n\n")
		writeFile(readmeFileName, "> Tech Specs: " + value + "\n\n")
		writeFile(readmeFileName, "| Identifier | Device Name | \n| ---------- | ----------- |\n")

		jsonData = readJson(jsonFileName)
		for identifier, deviceName in jsonData.iteritems():
			writeFile(readmeFileName, "| " +identifier+ " | "+deviceName+"  |\n")

		writeFile(readmeFileName, "\n")

if __name__ == "__main__":
    main()
