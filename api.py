from setting import *

openport = os.environ['PORT']
# openport = 8765
print("[INFO] START WITH PORT : ",openport)

app = Flask(__name__)
CORS(app)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-impl-side-painting')
chrome_options.add_argument('--disable-gpu-sandbox')
chrome_options.add_argument('--disable-accelerated-2d-canvas')
chrome_options.add_argument('--disable-accelerated-jpeg-decoding')
chrome_options.add_argument('--test-type=ui')
chrome_options.add_argument('--disable-dev-shm-usage') #fixing crash tab
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content') #Enable java script
chrome_options.add_argument('--window-size=1024x800')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0')
# chrome_options.add_argument("--disable-extensions")


@app.route('/')
def main():
	
	name ="Youtube Crawler Engine"
	version = "v1"
	port = openport

	result = {
		"name":name,
		"version":version,
		"port":port
	} 


	return json.dumps(result)


@app.route('/youtube', methods=['GET'])
def get_url():

	datetime_crawling_ms = int(datetime.datetime.now().strftime("%s")) * 1000

	
	driver = webdriver.Chrome(chrome_options=chrome_options)

	if 'sp' in request.args:
		sp = request.args["sp"]
	else:
		sp = "CAISBAgBEAE%253D"

	keyword = request.args["keyword"]
	# keyword = "penusukan wiranto"

	url = "https://www.youtube.com/results?search_query="+keyword+"&sp="+sp
	# url = "https://www.youtube.com/results?search_query=aswkddodo&sp=EgIIAQ%253D%253D"
	# driver.get("https://m.youtube.com/?persist_app=0&app=dekstop")
	print(url)
	driver.get(url)
	

	# last_height = driver.execute_script("return document.body.scrollHeight")
	# print("[INFO] START Height",last_height)

	# while True:
	# 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	# 	time.sleep(3.5)
	# 	new_height = driver.execute_script("return document.body.scrollHeight")
	# 	print("[SUCCESS] SCROOL",last_height,new_height)
	# 	if new_height == last_height:
	# 		break
	# 	last_height = new_height
	# return driver.page_source

	if ("Coba kata kunci lain atau hapus filter penelusuran" in driver.page_source):
		print("[INFO] KATA KUNCI "+keyword+" TIDAK DI TEMUKAN")
		# return driver.page_source
		return json.dumps({"status":1,"results":None})
 
	


	try:
		results = []
		count = 0
		
		for x in driver.find_elements_by_xpath("//ytd-video-renderer"):
			
			count = count+1
			publish_time = None
			publish_time_text = None
			try:
				for y in driver.find_element_by_id("metadata-line").find_elements_by_class_name("style-scope.ytd-video-meta-block"):
					if "menit" in y.text:
						publish_time = datetime_crawling_ms-((int(y.text.replace(" menit yang lalu",""))*60)*1000)
						publish_time_text = y.text
					if "detik" in y.text:
						publish_time = datetime_crawling_ms-(int(y.text.replace(" detik yang lalu",""))*1000)
						publish_time_text = y.text

			except Exception as e:
				print(e)
			

			try:
				video_id= x.find_element_by_id("video-title").get_attribute("href")
				video_id = video_id.split("=")[1]
			except Exception as e:
				video_id = None
				print(e)
			
			try:
				video_title = x.find_element_by_id("video-title").text
			except Exception as e:
				video_title = None
				print(e)
			
			try:
				description = x.find_element_by_id("description-text").text
			except Exception as e:
				description = None
				print(e)

			try:
				description_html = x.find_element_by_id("description-text").get_attribute("outerHTML")
			except Exception as e:
				description_html = None
				print(e)

			try:
				channel_id = x.find_element_by_class_name("yt-simple-endpoint.style-scope.yt-formatted-string").get_attribute("href")
				channel_id = channel_id.replace("https://www.youtube.com/channel/","")
			except Exception as e:
				channel_id = None
				print(e)
			try:
				channel_title = x.find_element_by_class_name("style-scope.ytd-channel-name.complex-string").text
			except Exception as e:
				channel_title = None
				print(e)
			
			try:
				thumbnails = x.find_element_by_class_name("style-scope.yt-img-shadow").get_attribute("src")
			except Exception as e:
				thumbnails = None
				print(e)

			

			# print(json.dumps({
			# 	"count":count,
			# 	"datetime_crawling_ms":datetime_crawling_ms,
			# 	"publish_time":publish_time,
			# 	"publish_time_text":publish_time_text,
			# 	"video_id":video_id,
			# 	"video_title":video_title,
			# 	"description":description,
			# 	"description_html":description_html,
			# 	"channel_id":channel_id,
			# 	"channel_title":channel_title,
			# 	"thumbnails":thumbnails
				
			# 	}))

			results.append({
				"datetime_crawling_ms":datetime_crawling_ms,
				"publish_time":publish_time,
				"publish_time_text":publish_time_text,
				"video_id":video_id,
				"video_title":video_title,
				"description":description,
				"description_html":description_html,
				"channel_id":channel_id,
				"channel_title":channel_title,
				"thumbnails":thumbnails

				})
		status = 1
	except Exception as e:
		status = 0
		results = None
		print(e)
	
	# html = driver.page_source
	driver.execute_script('window.localStorage.clear();')


	# driver.close()
	driver.quit()
	return json.dumps({"status":status,"results":results})
	# return html

 

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=openport, debug=False, threaded=True)
	
	