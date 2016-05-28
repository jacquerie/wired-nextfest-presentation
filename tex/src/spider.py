class SenatoSpider(scrapy.Spider):

    """A spider to download all amendments of a law discussed by the Italian Senate."""

    name = 'senato'
    allowed_domains = ['senato.it']
    start_urls = ['http://www.senato.it/leg/17/BGT/Schede/Ddliter/testi/46051_testi.htm']

    def parse(self, response):
        for href in response.xpath(AMENDMENT_XPATH).extract():
            match = re.search(HREF_REGEX, href)
            if match:
                _id = match.group('_id')
                parent = match.group('parent')
                relative_url = AMENDMENT_URL.format(_id=_id, parent=parent)
                absolute_url = response.urljoin(relative_url)
                yield scrapy.Request(absolute_url, callback=self.download_amendment)

    def download_amendment(self, response):
        relative_filename = response.url.split('/')[-1]
        absolute_filename = os.path.join(os.getcwd(), 'data', relative_filename)
        with open(absolute_filename, 'wb') as f:
            f.write(response.body)
