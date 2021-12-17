import os.path
import xml.sax


BASE_PATH = os.path.dirname(__file__)

class StreamDataGenerator(xml.sax.handler.ContentHandler):

  lastEntry = None
  readingText  = False

  def parse_xml(self, f):
    self.readingText = False
    for l in f:
      if l.strip().startswith("<doc>"):
        self.lastEntry = {"abstract": "", "title": "", "url": ""}
        continue
      if l.strip().startswith("<title>"):
        self.lastEntry["title"] = l.replace("<title>", "").replace("</title>", "").strip()
        continue
      if l.strip().startswith("<abstract>"):
        self.lastEntry["abstract"] = l.replace("<abstract>", "").replace("</abstract>", "").strip()
        continue
      if l.strip().startswith("<url>"):
        self.lastEntry["url"] = l.replace("<url>", "").replace("</url>", "").strip()
        continue
      if l.strip().startswith("</doc>"):
        yield self.lastEntry
        self.lastEntry = {}
        continue
      if l.strip().startswith("</feed>"):
        raise StopIteration
      
  def parse(self):
    parser = xml.sax.make_parser()
    parser.setContentHandler(self)
    f = open(os.path.join(BASE_PATH, "enwiki-20210720-abstract.xml"))
    return self.parse_xml(f)

