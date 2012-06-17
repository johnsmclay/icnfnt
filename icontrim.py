# all the imports
#import sqlite3
from flask import Flask, request
import os.path

### configuration ###

## Database
#DATABASE = '/tmp/flaskr.db'
#DEBUG = True
#SECRET_KEY = 'development key'
#USERNAME = 'admin'
#PASSWORD = 'default'

## Application
FONT_FILE = 'fontawesome-webfont.ttf'
TMP_FILE_DIR = 'tmp'
DOWNLOAD_DIR = 'download'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/api/createpack', methods=['POST'])
def createpack():
    json_data = request.form['json_data']
    #json_data = open('fontawesome.json').read()
    import json, time, random
    request_data = json.loads(json_data)
    identifier = ''.join([str(time.time()),'-',str(random.randint(0, 99999))])
    dir = os.path.join(os.curdir, TMP_FILE_DIR, identifier)
    if not os.path.exists(dir):
        os.makedirs(dir)
    identifier = create_subfont(identifier,request_data)

    response = app.make_response(''.join(['/api/downloadpack/',identifier]))

    return response

@app.route('/api/downloadpack/<identifier>')
def downloadpack(identifier):
    zipfile = os.path.join(os.curdir, DOWNLOAD_DIR, ''.join([identifier,'.zip']) )
    response = app.make_response(open(zipfile).read())
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] = 'attachment; filename="customfont.zip"'

    os.remove(zipfile)

    return response

def create_subfont(identifier,req_chars):
    import fontforge

	#font & family & file name
    name = ''.join(['bootstrap_subfont',identifier])

	#set up the font
    f = fontforge.open('fonts/fontawesome-webfont.ttf')
    f.fontname = name
    f.familyname = name
    f.fondname = name
    f.fullname = name

	#set up the less file
    less_data = open('font-awesome.less.template').read()
    less_out_file = open(os.path.join(os.curdir, TMP_FILE_DIR, identifier, ''.join([name,'.less'])),'w')
    less_out_file.write(less_data)

	# Select all the chars we want
    for character in req_chars:
        # write the char to the less file
        less_out_file = open(os.path.join(os.curdir, TMP_FILE_DIR, identifier, ''.join([name,'.less'])),'a')
        less_out_file.write(''.join(['.icon-',str(character['name']),':before',"\t\t",'{ content: "\\f',str(character['uni']),'"; }',"\n"]))
        # select it in fontforge
        f.selection.select(("more","unicode",None),''.join(['uniF',str(character['uni'])]))

	# Invert the selection
    f.selection.invert()

	# Remove the selected objects
    f.cut()

	#kick out an otf
    filetypes = [	'ttf',
					'eot',
					'woff',
					'svg',
				]

    for filetype in filetypes:
		f.generate(os.path.join(os.curdir, TMP_FILE_DIR, identifier, ''.join([name, '.', filetype])))

    import subprocess
    PIPE = subprocess.PIPE
    zipfile = os.path.join(os.curdir, DOWNLOAD_DIR, ''.join([identifier,'.zip']))
    pd = subprocess.Popen(['/usr/bin/zip', '-r', '-j', zipfile, os.path.join(os.curdir, TMP_FILE_DIR, identifier)], stdout=PIPE, stderr=PIPE) 
    stdout, stderr = pd.communicate()

    # delete the files created so they don't take up space
    import shutil
    shutil.rmtree(os.path.join(os.curdir, TMP_FILE_DIR, identifier))

    return identifier


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')
