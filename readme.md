# Make a readable PDF version of a website

Convert a website into a PDF file for later offline reading 
and annotation.  This is simlar to most browsers' "Reading View" of a website.
This is something that started with Instapaper, the Arc90 Project, and 
Safari version 5.

*  https://www.ctrl.blog/entry/browser-reading-mode-parsers#
*  http://ejucovy.github.io/readability/
*  https://en.wikipedia.org/wiki/Readability_(service)
*  https://github.com/masukomi/arc90-readability

Quite a few article extractors are available today. 
After briefly testing a few, the Goose extractor worked 
the best for my requirements

*  https://github.com/goose3/goose3 
*  https://goose3.readthedocs.io/en/latest/code.html#article 


## How to convert

  (1) put a list of urls into a file, one to a line, or pipe them directly 
      into the python program (see examle list.txt)

  (2) extract the articles using the python program Honker.py, which
      uses Goose3.  The optional numeric argument is for the output
      filenames, which are numbers like: news000.md, news001.md, etc.

      `$ cat list.txt | python3 honker.py [33]`

  (3) convert the markdown files to PDF using pandoc, which uses some
      latex customization templates. This script won't overwrite a
      PDF file, so erase them first.

      `$ md2pdf.sh news???.md` 

  (4) if desired, merge the pdfs into one, using a utitlity such as

      `$ pdfunite news???.pdf merged.pdf`



