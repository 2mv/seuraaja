import sys

from downloader import Downloader
from converter import Converter
from analysis_parser import AnalysisParser
from recommendations import Recommendations
from mailer import Mailer
from discoverer import Discoverer


import logger


logger.info("Begin analysis URL discovery")
morning_analysis_url = Discoverer.determine_analysis_url()
logger.info("Begin analysis file download from %s" % morning_analysis_url)
with Downloader.download_to_tmp(morning_analysis_url) as analysis_file:
  analysis_xml = Converter.to_xml(analysis_file)
logger.info("Begin analysis file parsing")
company_summaries = AnalysisParser.get_company_summaries(analysis_xml)

current_recommendations = Recommendations.get_current_recommendations(company_summaries)
last_recommendations = Recommendations.read_stored_recommendations()
last_recommendations = [] if last_recommendations is None else last_recommendations
changed_recommendations = Recommendations.get_changed_recommendations(current_recommendations, last_recommendations)
new_recommendations = Recommendations.get_new_recommendations(current_recommendations, last_recommendations)

if len(changed_recommendations) > 0 or len(new_recommendations) > 0:
  logger.info("Changed recommendations: %s" % repr(changed_recommendations))
  logger.info("New recommendations: %s" % repr(new_recommendations))
  try:
    to_addr = sys.argv[1]
    logger.info("Begin sending email to %s" % to_addr)
    Mailer.send_recommendations(changed_recommendations, new_recommendations, to_addr)
  except IndexError:
    logger.info("No email address to send results to provided. Skipping.")
else:
  logger.info("No new or changed recommendations")

logger.info("Saving recommendations to file")
Recommendations.persist(current_recommendations)

logger.info("Done")
