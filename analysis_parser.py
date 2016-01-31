from bs4 import BeautifulSoup
from bs4.element import NavigableString


class AnalysisParser:

  SUMMARY_LINE_ORDER = ['name', 'close', 'change', 'ytd', 'recommendation', 'goal', 'potential',
                        'p_e_last_year', 'ev_ebit_last_year', 'p_e_this_year', 'ev_ebit_this_year',
                        'p_b_last_year', 'dividend', 'revenue_percent', 'mcap']

  @staticmethod
  def get_company_summaries(analysis_xml):
    soup = BeautifulSoup(analysis_xml, "html5lib")
    summaries = []
    for page in soup.pages:
      summaries += AnalysisParser.get_page_summaries(page)
    return summaries

  @staticmethod
  def get_page_summaries(page):
    if not AnalysisParser.is_summary_page(page):
      return []

    lines = AnalysisParser.get_parsed_lines(page)
    summaries = []
    for line in lines:
      if line[-1] == unicode('MCAP'):  # Table group heading
        continue
      elif line[0] == unicode('Mediaani'):  # Table group summary
        continue
      elif len(line) != len(AnalysisParser.SUMMARY_LINE_ORDER):  # Line is wrong length for a summary line
        continue
      else:  # Should be a summary line
        summaries.append(AnalysisParser.line_to_summary(line))
    return summaries

  @staticmethod
  def is_summary_page(page):
    lines = AnalysisParser.get_parsed_lines(page)
    for line in lines:
      if line[-1] == unicode('MCAP'):  # Table group heading
        return True
    return False

  @staticmethod
  def get_parsed_lines(page):
    tabular_lines = AnalysisParser.get_tabular_lines(page)
    return [AnalysisParser.get_words(line) for line in tabular_lines]

  @staticmethod
  def get_tabular_lines(page):
    if isinstance(page, NavigableString):  # page content was just a string
      return []
    lines = {}
    for text in page.select('figure text'):
        line_id = text['bbox'].split(',')[1]
        line = lines.get(line_id, [])
        line.append(text)
        lines[line_id] = line
    return lines.values()

  @staticmethod
  def get_words(line, word_offset=6.5):
    words = []
    previous_offset = None
    for text in line:
        current_offset = float(text['bbox'].split(',')[0])
        if previous_offset is None or previous_offset < current_offset - word_offset:
            words.append(text.get_text())
        else:
            words[-1] += text.get_text()
        previous_offset = current_offset
    return words

  @staticmethod
  def line_to_summary(line):
    return dict(zip(AnalysisParser.SUMMARY_LINE_ORDER, line))
