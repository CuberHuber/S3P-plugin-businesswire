import datetime
from logging import config

import pytz
from selenium import webdriver

from businesswire import BusinessWire
from src.spp.types import SPP_document

config.fileConfig('dev.logger.conf')


def driver():
    """
    Selenium web driver
    """
    options = webdriver.ChromeOptions()

    # Параметр для того, чтобы браузер не открывался.
    options.add_argument('headless')

    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    return webdriver.Chrome(options)

# doc = SPP_document(id=None, title='Valley Forge Fabrics: Weaving in cloud-based efficiency from quote to install', abstract='What is cloud operational efficiency? For VFF, it’s a Microsoft solution that streamlines operations, improves customer experiences and supports growth.', text=None, web_link='https://www.pwc.com/gx/en/ghost/valley-forge-fabrics-cloud-efficiency.html', local_link=None, other_data=None, pub_date=datetime.datetime(2023, 11, 15, 0, 0), load_date=datetime.datetime(2024, 3, 19, 13, 53, 25, 455015))
doc = SPP_document(id=None, title='Regula and RADEX BCMS Collaborate to Enhance Caribbean Border Control with Swift Identity Verification', abstract=None, text='RESTON, Va.--(BUSINESS WIRE)--The Aruban Immigration Authority has set up an online Embarkation and Disembarkation (ED) program to facilitate the process of passport control at the border. Using this system, travelers obtain online entry permission before flying to Aruba. This procedure allows the Aruban authorities to gather necessary data beforehand, allowing travelers to enjoy smooth and fast document processing at the border while maintaining a high level of security.\nRADEX BCMS has successfully developed and integrated an effective border management solution in Aruba. For the initial release, they partnered with a vendor which provided document readers; however, while they aimed for excellence, they encountered challenges, as the readers did not fully meet their high expectations, primarily due to extended processing times and service-related issues. To improve the workflow of their border control management system, RADEX BCMS substituted the previous devices with Regula flagship document readers.\nNow, the Regula 7034M is a cornerstone for comprehensive identity verification (IDV) — it instantly scans a passport page and automatically checks major security features in white, infrared, ultraviolet, and coaxial lights. The advanced optical character recognition, trained to work with identity documents, recognizes all sorts of data, including engraved and embossed text. Smart algorithms instantly read data from barcodes and machine-readable zones, as well as RFID chips.\nBy leveraging the advanced technologies provided by Regula & RADEX BCMS, the Aruban authorities have succeeded in decreasing document verification time at border crossings by an impressive 300%. Now, it takes only 10 seconds to process a passport. As a result, travelers benefit from expedited admissions, while authorities can effectively manage and screen incoming travelers.\n“Our collaboration with Regula has been truly fruitful. By significantly reducing the time needed for identity verification at our borders, we not only enhance the efficiency of border management but also significantly improve the travel experience for thousands of individuals. This success reflects our commitment to leveraging innovative solutions to meet the demands of modern security and mobility, ensuring that safety and convenience go hand-in-hand. We are looking forward to extending our partnership and growing new experience with Regula,” says Frank Baks, Director at RADEX BCMS.\n“As a company with over 30 years of experience developing IDV hardware and software, we always welcome the opportunity to participate in projects which require complete solutions for border management. This gives us a chance not only to contribute our accumulated knowledge, but also to learn and gather more information to develop future products. Aruba is an example of a unique system that, on the one hand, makes visitors feel welcome by providing them with fast and less stressful border crossing, and, on the other hand, maintains a solid system of checking and verification,” says Arif Mamedov, President and CEO at Regula Forensics, Inc.\nAbout RADEX BCMS\nRADEX BCMS develops state-of-the-art software for border control management, immigration platforms for pre-enrollment of travelers, Tourism Information Systems, and eGoverment solutions. Their main solution is a complete border control management system (BCMS) developed with the latest hardware and software for multi-biometric capture and search capabilities. The system is an application with an extensive array of modules that is developed as a turnkey solution to assist government agencies involved in law enforcement activities and protection of country borders.\nLearn more at http://www.radexbcms.com.\nAbout Regula\nRegula is a global developer of forensic devices and identity verification solutions. With our 30+ years of experience in forensic research and the largest library of document templates in the world, we create breakthrough technologies in document and biometric verification. Our hardware and software solutions allow over 1,000 organizations and 80 border control authorities globally to provide top-notch client service without compromising safety, security or speed. Regula has been repeatedly named a Representative Vendor in the Gartner® Market Guide for Identity Verification.\nLearn more at www.regulaforensics.com.', web_link='https://www.businesswire.com/news/home/20240327438067/en/Regula-and-RADEX-BCMS-Collaborate-to-Enhance-Caribbean-Border-Control-with-Swift-Identity-Verification', local_link=None, other_data=None, pub_date=datetime.datetime(2024, 3, 27, 3, 0, tzinfo=pytz.UTC), load_date=None)

parser = BusinessWire(driver(), 10, doc)
docs: list[SPP_document] = parser.content()


print(*docs, sep='\n\r\n')
