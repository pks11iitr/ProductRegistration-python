from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch,cm

class ProductRegistration:

    def parse_obj(self, lt_objs):

        # loop over the object list
        for obj in lt_objs:

            if isinstance(obj, pdfminer.layout.LTTextLine):
                print( "%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_')))

            # if it's a textbox, also recurse
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                self.parse_obj(obj._objs)

            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                self.parse_obj(obj._objs)

    def parsepdf(self, filename, startpage, endpage):

        # Open a PDF file.
        fp = open(filename, 'rb')

        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        document = PDFDocument(parser)

        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # Create a PDF device object.
        device = PDFDevice(rsrcmgr)

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        laparams = LAParams()

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

            # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)


        i = 0
        # loop over all pages in the document
        for page in PDFPage.create_pages(document):
            if i >= startpage and i <= endpage:
                # read the page into a layout object
                interpreter.process_page(page)
                layout = device.get_result()

                # extract text from this object
                self.parse_obj(layout._objs)
            i += 1

    def add_image (self,file, x, y):

        # # there are 66 slides (1.jpg, 2.jpg, 3.jpg...)
        # path = '/home/omsairam6/sign.png'
        # pdf = PdfFileWriter()
        #
        # #for num in range(1, 67):  # for each slide
        #     # Using ReportLab Canvas to insert image into PDF
        # imgTemp = BytesIO()
        # imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
        # # Draw image on Canvas and save PDF in buffer
        # imgDoc.drawImage(path, x, y)
        # # x, y - start position
        # # in my case -25, -45 needed
        # imgDoc.save()
        # # Use PyPDF to merge the image-PDF into the template
        # pdf.addPage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))
        #
        # pdf.write(open("", "wb"))

        c = canvas.Canvas('test.pdf')
        # move the origin up and to the left
        c.translate(inch, inch)
        c.setFillColorRGB(1, 0, 1)
        #c.drawImage("/home/omsairam6/sample.png", 2, 2, 50, 50)
        c.drawImage("/home/omsairam6/sign.png", x, y,25,50)
        c.showPage()
        c.save()

        # Get the watermark file you just created
        watermark = PdfFileReader(open("test.pdf", "rb"))

        # Get our files ready
        output_file = PdfFileWriter()
        input_file = PdfFileReader(open(file, "rb"))

        # Number of pages in input document
        page_count = input_file.getNumPages()

        # Go through all the input file pages to add a watermark to them
        for page_number in range(page_count):
            print("Watermarking page {} of {}".format(page_number, page_count))
            # merge the watermark with the page
            input_page = input_file.getPage(page_number)
            input_page.mergePage(watermark.getPage(0))
            # add page from input file to output document
            output_file.addPage(input_page)

        # finally, write "output" to document-output.pdf
        with open("output.pdf", "wb") as outputStream:
            output_file.write(outputStream)

    def start(self, file):
        pdf = PdfFileReader(open(file, 'rb'))
        pages=pdf.getNumPages()
        self.parsepdf(file, 0, pages-1)
        self.add_image(file, 422,58)

pdf_parser=ProductRegistration()
pdf_parser.start('/home/omsairam6/sample.pdf')
#pdf_parser.add_image('/home/omsairam6/sample.pdf', 0, 0)