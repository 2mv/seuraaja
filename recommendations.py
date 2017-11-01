import unicodecsv as csv
import tempfile
import os
import errno


from datetime import date


class Recommendations:

  STORED_RECOMMENDATIONS_FILENAME = os.path.join(tempfile.gettempdir(), 'seuraaja_recommendations_last.csv')
  CSV_FIELD_NAMES = ['name', 'recommendation', 'potential', 'timestamp']

  @staticmethod
  def company_summary_to_recommendation(company_summary):
    return {
        'name': company_summary['name'],
        'recommendation': company_summary['recommendation'],
        'potential': company_summary['potential'],
        'timestamp': date.today()
    }

  @staticmethod
  def get_current_recommendations(company_summaries):
    return map(Recommendations.company_summary_to_recommendation, company_summaries)

  @staticmethod
  def read_stored_recommendations():
    try:
      with open(Recommendations.STORED_RECOMMENDATIONS_FILENAME, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
    except IOError as e:
      if e.errno == errno.ENOENT:
        return None
      raise e

  @staticmethod
  def get_changed_recommendations(current_recommendations, last_recommendations):
    last_company_names = map(lambda r: r['name'], last_recommendations)
    last_recommendations_by_name = dict(zip(last_company_names, last_recommendations))
    return filter(lambda r: r['name'] in last_recommendations_by_name and
                  last_recommendations_by_name[r['name']]['recommendation'] != r['recommendation'],
                  current_recommendations)

  @staticmethod
  def get_new_recommendations(current_recommendations, last_recommendations):
    current_company_names = map(lambda r: r['name'], current_recommendations)
    last_company_names = map(lambda r: r['name'], last_recommendations)
    new_company_names = set(current_company_names) - set(last_company_names)
    return filter(lambda r: r['name'] in new_company_names, current_recommendations)

  @staticmethod
  def persist(recommendations):
    with open(Recommendations.STORED_RECOMMENDATIONS_FILENAME, 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=Recommendations.CSV_FIELD_NAMES)
      writer.writeheader()
      for recommendation in recommendations:
        writer.writerow(recommendation)
