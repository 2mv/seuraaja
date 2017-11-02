import requests
import re


from bs4 import BeautifulSoup


from downloader import Downloader


class Discoverer:

  ANALYSIS_OPENER_URL = "http://bit.ly/Inderes-aamukirje-NN"

  @staticmethod
  def determine_analysis_url():
    with Downloader.download_to_tmp(Discoverer.ANALYSIS_OPENER_URL) as analysis_page:
      analysis_page.seek(0)
      soup = BeautifulSoup(analysis_page.read(), "html5lib", from_encoding='utf-8')
    return soup.find_all('a', href=re.compile('aamukatsaus.*\.pdf$'))[0]['href']
