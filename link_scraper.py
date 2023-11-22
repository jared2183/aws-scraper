import scrapy
import validators
from urllib.parse import urlparse

class LinkSpider(scrapy.Spider):
    name = "links"
    start_urls = [
        "https://www.fda.gov/",
        "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/search/default.cfm",
        "https://www.fda.gov/medical-devices/cdrh-international-programs/international-medical-device-regulators-forum-imdrf",
        "https://www.fda.gov/medical-devices/digital-health-center-excellence/software-medical-device-samd",
        "https://www.fda.gov/medical-devices/cdrh-international-programs/medical-device-single-audit-program-mdsap",
        "https://ec.europa.eu/health/sites/default/files/md_sector/docs/mdcg_2021-24_en.pdf",
        "https://ec.europa.eu/health/md_sector/overview_en",
        "https://www.canada.ca/en/health-canada/services/drugs-health-products/medical-devices.html",
        "https://www.canada.ca/en/health-canada/services/drugs-health-products/medical-devices/application-information/guidance-documents/guidance-document-guidance-risk-based-classification-system-non-vitro-diagnostic.html",
        "https://www.tga.gov.au/publication/australian-regulatory-guidelines-medical-devices-argmd"
    ]

    def parse(self, response):
        home_url = response.request.url

        # finds all valid and external links
        for url in response.xpath("//a/@href").getall():
            if url is not None and home_url is not None:
                if validators.url(url) and url not in home_url:
                    domain = urlparse(url).netloc
                    print(domain, end=", ")
                    yield {'domain': domain}