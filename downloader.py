import requests

import tempfile


class Downloader:

  @staticmethod
  def download_to_tmp(url):
    target_file = tempfile.NamedTemporaryFile(mode='w+b')
    response = requests.get(url, stream=True)
    for chunk in response.iter_content():
      target_file.write(chunk)
    return target_file
