from crawl4ai import WebCrawler

# Create an instance of crawler
crawler = WebCrawler()
# Warm up the crawler (load necessary models)
crawler.warmup()

urls = [
    {"name": "UND Homepage", "url": "https://und.edu"},
    {"name": "Campus UND", "url": "https://campus.und.edu/"},
    {"name": "UND Alumni", "url": "https://undalumni.org/"},
    {"name": "Microsoft Login", "url": "https://login.microsoftonline.com/"},
    {"name": "Blackboard UND", "url": "https://blackboard.und.edu"},
    {"name": "Student Admin Login", "url": "https://studentadmin.connectnd.us/NDCSPRD/signon.html"},
    {"name": "HCM Login", "url": "https://prd.hcm.ndus.edu/psp/hehp/?cmd=login"},
    {"name": "Civitas Learning Login", "url": "https://und.inspire.civitaslearning.com/login"},
    {"name": "UND Civitas DM", "url": "https://unddm.civitaslearning.com/"},
    {"name": "UND Zoom", "url": "https://und.zoom.us/"},
    {"name": "UND Campus Directory", "url": "https://campus.und.edu/directory/index.html"},
    {"name": "Fighting Hawks", "url": "https://fightinghawks.com/"},
    {"name": "UND Admissions Visit", "url": "https://und.edu/admissions/visit/index.html"},
    {"name": "UND Blog", "url": "https://blogs.und.edu/und-today/"},
    {"name": "UND Terms of Use", "url": "https://und.edu/about/terms-of-use.html#privacy"},
    {"name": "UND Instagram", "url": "https://www.instagram.com/uofnorthdakota/"},
    {"name": "UND Facebook", "url": "https://www.facebook.com/UofNorthDakota"},
    {"name": "UND YouTube", "url": "https://www.youtube.com/user/UofNorthDakota"},
    {"name": "UND LinkedIn", "url": "https://www.linkedin.com/school/9200/"},
    {"name": "UND Twitter", "url": "https://twitter.com/UofNorthDakota"},
    {"name": "UND Events Calendar", "url": "https://calendar.und.edu/"},
    {"name": "UND Careers", "url": "https://campus.und.edu/human-resources/careers/index.html"},
    {"name": "UND Alumni Org", "url": "https://undalumni.org/"},
    {"name": "SafeUND", "url": "https://campus.und.edu/safety/safeund/index.html"},
    {"name": "UND Feedback", "url": "https://und.edu/about/website-feedback.html"},
    {"name": "UND Terms", "url": "https://und.edu/about/terms-of-use.html"},
    {"name": "Equal Opportunity Notices", "url": "https://campus.und.edu/equal-opportunity/required-notices.html#notice-of-nondiscrimination"},
    {"name": "Student Disclosure Info", "url": "https://und.edu/about/student-disclosure-information/index.html"},
    {"name": "UND Equal Opportunity", "url": "https://campus.und.edu/equal-opportunity/index.html"},
    {"name": "Omniupdate UND", "url": "https://a.cms.omniupdate.com/11/?skin=und&account=UND&site=und&action=de&path=/index.pcf"}
]

# Iterate over the list of URLs and save results to a text file
results = []  # Store results for each URL
with open('crawler_results.txt', 'w', encoding='utf-8') as file:  # Set encoding to 'utf-8'
    for item in urls:
        result = crawler.run(item['url'])  # Pass individual URL to crawler.run()
        results.append(result)

        # Write results to the text file
        file.write(f"Results for {item['name']} ({item['url']}):\n")
        
        # Check if result.markdown is not None before writing
        if result.markdown:
            file.write(result.markdown)  # Save the result in markdown format
        else:
            file.write("No content found for this URL.\n")  # Write a message if no content is found
        
        file.write("\n\n")  # Add spacing between entries

print("Results saved to crawler_results.txt")
