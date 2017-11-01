from StringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


class Converter:

    @staticmethod
    def to_xml(infile):
        output = StringIO()
        manager = PDFResourceManager()
        converter = XMLConverter(manager, output, laparams=LAParams(), codec='utf-8')
        interpreter = PDFPageInterpreter(manager, converter)

        for page in PDFPage.get_pages(infile):
            interpreter.process_page(page)
        converter.close()
        xml = output.getvalue()
        output.close
        return xml
