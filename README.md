
## Python Web Scraper for (Resurva Clients)

#### Requirements:

 - Chrome Driver
	- Mac users with Homebrew installed:  `brew install chromedriver`
	- Debian based Linux distros:  `sudo apt-get install chromium-chromedriver`
	- Windows users with Chocolatey installed:  `choco install chromedriver`
 - Python 3.5
				
				
#### Installation:
- Clone Repo
- Go to project folder.
	> cd project_folder
- Make a virtual environment
	> virtualenv venv
- Activate environment
	- (FOR MAC/LINUX)
		> source venv/bin/activate
	- (FOR WINDOWS)
		> venv\Scripts\activate
- Install packages
		> pip install -r requirements.txt
- SET RESURVA `USERNAME` and `PASSWORD` in ```
project_name/scraper/settings.py
```
- Open Terminal/CMD
	Type
		> cd project_name/scraper
		> scraper crawl client -o client.json -a tag=client
- Check `project_name/scraper/client.json` for expored client data
