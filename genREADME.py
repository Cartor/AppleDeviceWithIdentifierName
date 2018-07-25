import datetime, json, os
import settings

def writeFile(filename, data):
	with open(filename, 'a') as outfile:
		outfile.write(data.encode('utf-8'))

def readJson(filename):
	with open(filename) as f:
		data = json.load(f)
		return data

def main():
	readmeFileName = "README.md"
	os.remove(readmeFileName)

	MDData = "# AppleDeviceWithIdentifierName\n\
Apple device's name map model Identifier (Mac)\n\
\n\
"
	writeFile(readmeFileName, MDData)

	for attr, value in settings.MacInfoURL.iteritems():
		print attr, value
		jsonFileName = "json/" + attr.replace(' ', '_') + ".json"

		writeFile(readmeFileName, "\n## [" + attr + "](" +jsonFileName+ ")\n\n")
		writeFile(readmeFileName, "> Tech Specs: " + value[0] + "\n\n")
		writeFile(readmeFileName, "| Identifier | Device Name | \n| ---------- | ----------- |\n")

		jsonData = readJson(jsonFileName)

		for identifier, deviceName in sorted(jsonData.iteritems(), key=lambda (k,v): (k,v)):
			writeFile(readmeFileName, "| " +identifier+ " | "+deviceName+"  |\n")

		writeFile(readmeFileName, "\n")

if __name__ == "__main__":
    main()
