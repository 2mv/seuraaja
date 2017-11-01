import sys

from downloader import Downloader
from converter import Converter
from analysis_parser import AnalysisParser
from recommendations import Recommendations
from mailer import Mailer


try:
  morning_analysis_url = sys.argv[1]
except IndexError:
  print("Please provide analysis file URL as first argument")
  sys.exit(1)

with Downloader.download_to_tmp(morning_analysis_url) as analysis_file:
  analysis_xml = Converter.to_xml(analysis_file)
company_summaries = AnalysisParser.get_company_summaries(analysis_xml)

current_recommendations = Recommendations.get_current_recommendations(company_summaries)
last_recommendations = Recommendations.read_stored_recommendations()
last_recommendations = [] if last_recommendations is None else last_recommendations
changed_recommendations = Recommendations.get_changed_recommendations(current_recommendations, last_recommendations)
new_recommendations = Recommendations.get_new_recommendations(current_recommendations, last_recommendations)

if len(changed_recommendations) > 0 or len(new_recommendations) > 0:
  try:
    to_addr = sys.argv[2]
  except IndexError:
    print("Please provide email address to send results to as second argument")
    sys.exit(1)
  Mailer.send_recommendations(changed_recommendations, new_recommendations, to_addr)

Recommendations.persist(current_recommendations)
