#!/usr/bin/python3

import urllib.request , re , time , sys

def GetPages(TheURL , TheURL2 , NumberOfPages):
	'''Finds the URLs of all the pages in an Instagram account'''

	Pages = list()
	Pages.append(TheURL)

	for repeat in range(NumberOfPages):
		try:
			page = urllib.request.urlopen(TheURL2)

			for line in page:
				line = line.decode()
				load = re.findall('"end_cursor":\s"([A-Za-z0-9].*?)"' , line)
				if load == []:
					continue
				else:
					TheURL2 = TheURL + '/?max_id=' + load[0]
					Pages.append(TheURL2)

		except Exception as TheError:
			print('[-] Error in getting account pages')
			print(TheError)
			continue

	return(Pages)



def GetVideos(URL):
	'''Takes the URL of an Instagram page and finds all the .mp4 video links in it and returns a list of all these video links'''

	instagram = urllib.request.urlopen(URL)

	videos = list()
	for line in instagram:
		line = line.decode()
		link = re.findall('"code":\s"(.*?)"' , line)
		if link == []:
			continue
		else:
			for code in link:
				try:
					posturl = 'https://www.instagram.com/p/' + code
					instagram2 = urllib.request.urlopen(posturl)
					for line in instagram2:
						line = line.decode()
						link = re.findall('"video_url":\s"(.*?)",' , line)
						if link == []:
							continue
						else:
							instalink = link[0]
							videos.append(instalink)
							break

				except Exception as TheError:
					print('[-] Error in getting video links')
					print(TheError)
					time.sleep(1)
					continue

	return(videos)
#----------------------------------------------------------------------------------------------------------------------------------
URL = sys.argv[1]
ListOfPages = GetPages(URL , URL , int(sys.argv[2]))

count=0
for page in ListOfPages:
	ListOfVideos = GetVideos(page)
	count +=1
	print('Finished Page', count)
	for URLs in ListOfVideos:
		TheFile = open('Videos' , 'a')
		TheFile.write(URLs + '\n')
		TheFile.close()
