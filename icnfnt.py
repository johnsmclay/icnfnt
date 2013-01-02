"""
    icnfnt
    ~~~~~~~~~

    A utility for creating subsets of the FontAwesome icon font (by Dave Gandy)

    :copyright: (c) 2012 by Grant Gordon and Clay Johns.
    :license: TBD
"""

from flask import Flask, request
import os.path

### Configuration ###

## Application
FONT_FILE = 'fontawesome-webfont.ttf'
TMP_FILE_DIR = 'tmp'
DOWNLOAD_DIR = 'download'
ADMINS = ['grantjgordon@gmail.com', 'gwpc114@gmail.com']

## Create flask app
app = Flask(__name__)
app.config.from_envvar('ICNFNT_CONFIG')
#app.config.from_object(__name__)

if app.config['DEBUG']:
    from werkzeug import SharedDataMiddleware
    import os
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler(app.config['NOTIFICATION_SMTP_SERVER'], app.config['NOTIFICATION_FROM_ADDRESS'], ADMINS, 'YourApplication Failed')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


@app.route('/api/createpack', methods=['POST'])
def createpack():
    json_data = request.form['json_data']

    import json
    import time
    import random
    request_data = json.loads(json_data)
    identifier = ''.join([str(time.time()), '-', str(random.randint(0, 99999))])

    # Make the tmp folder
    dir = os.path.join(os.curdir, TMP_FILE_DIR, identifier)
    if not os.path.exists(dir):
        os.makedirs(dir)

    identifier = create_subfont(identifier, request_data)

    response = app.make_response(''.join(['/api/downloadpack/', identifier]))

    return response

@app.route('/api/downloadpack/<identifier>')
def downloadpack(identifier):
    zipfile = os.path.join(os.curdir, DOWNLOAD_DIR, ''.join([identifier, '.zip']))
    response = app.make_response(open(zipfile).read())
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] = 'attachment; filename="customfont.zip"'

    os.remove(zipfile)

    return response

def create_subfont(identifier,req_chars):
    import fontforge

    # Font & family & file name
    name = 'fontawesome'

    # Location of templates
    template_path = 'templates/'

    # Set up the font
    f = fontforge.open('fonts/fontawesome-webfont.ttf')
    f.fontname = name
    f.familyname = name
    f.fondname = name
    f.fullname = name

    # Set up the html test file
    html_data = open(''.join([template_path, 'test.html.template'])).read()
    html_out_file = open(os.path.join(os.curdir, TMP_FILE_DIR, identifier, 'icon-reference.html'), 'w')
    html_out_file.write(html_data)

    # Set up the less file
    less_data = open(''.join([template_path, 'font-awesome.less.template'])).read()
    less_out_file = open(os.path.join(os.curdir, TMP_FILE_DIR, identifier, ''.join([name, '.less'])), 'w')
    less_out_file.write(less_data)

    # Set up the ie compatibility less file
    lessie7_data = open(''.join([template_path, 'font-awesome-ie7.less.template'])).read()
    lessie7_out_file = open(os.path.join(os.curdir, TMP_FILE_DIR, identifier, ''.join([name, '-ie7.less'])), 'w')
    lessie7_out_file.write(lessie7_data)

    # Set up the sass file
    sass_data = open(''.join([template_path, 'font-awesome.sass.template'])).read()
    sass_out_file = open(os.path.join(os.curdir, TMP_FILE_DIR, identifier, ''.join([name, '.sass'])), 'w')
    sass_out_file.write(sass_data)

    # Set up the scss file
    scss_data = open(''.join([template_path, 'font-awesome.scss.template'])).read()
    scss_out_file = open(os.path.join(os.curdir, TMP_FILE_DIR, identifier, ''.join([name, '.scss'])), 'w')
    scss_out_file.write(scss_data)

    # Set up the css file
    css_data = open(''.join([template_path, 'font-awesome.css.template'])).read()
    css_out_file = open(os.path.join(os.curdir, TMP_FILE_DIR, identifier, ''.join([name, '.css'])), 'w')
    css_out_file.write(css_data)

    # Set up the ie compatibility css file
    cssie7_data = open(''.join([template_path, 'font-awesome-ie7.css.template'])).read()
    cssie7_out_file = open(os.path.join(os.curdir, TMP_FILE_DIR, identifier, ''.join([name, '-ie7.css'])), 'w')
    cssie7_out_file.write(cssie7_data)

    # Add each character we want to the font object and related style and html files
    for character in req_chars:
        html_out_file.write(''.join(['<tr><td><i class="icon-', str(character['name']), '"></i></td><td>.icon-', str(character['name']), '</td></tr>']))

        less_out_file.write(''.join(['.icon-', str(character['name']), ':before', "\t\t", '{ content: "\\f', str(character['uni']), '"; }', "\n"]))

        lessie7_out_file.write(''.join(['.icon-', str(character['name']), "\t\t", "{ .ie7icon('&#xf", str(character['uni']), ";'); }", "\n"]))

        sass_out_file.write(''.join(['.icon-', str(character['name']), ':before', "\n\t", 'content: "\\f', str(character['uni']), '"', "\n\n"]))

        scss_out_file.write(''.join(['.icon-', str(character['name']), ':before', "\t\t", '{ content: "\\f', str(character['uni']), '"; }', "\n"]))

        css_out_file.write(''.join(['.icon-', str(character['name']), ':before', "\t\t", '{ content: "\\f', str(character['uni']), '"; }', "\n"]))

        cssie7_out_file.write(''.join(['.icon-', str(character['name']), " { *zoom: expression( this.runtimeStyle['zoom'] = '1', this.innerHTML = '&#xf", str(character['uni']), ";&nbsp;'); }", "\n"]))

        f.selection.select(("more", "unicode", None), ''.join(['uniF', str(character['uni'])]))

    # Invert the selection
    f.selection.invert()

    # Remove the selected objects
    f.cut()

    # Kick out the various font files
    filetypes = [	'ttf',
                    'eot',
                    'woff',
                ]

    # Actually generate each of the font types
    for filetype in filetypes:
            f.generate(os.path.join(os.curdir, TMP_FILE_DIR, identifier, ''.join([name, '-webfont.', filetype])))

    f.close()

    # Add the closing line to the test.html file game
    html_out_file.write('</table></body></html>')

    # Close all the files
    html_out_file.close()
    less_out_file.close()
    lessie7_out_file.close()
    sass_out_file.close()
    scss_out_file.close()
    css_out_file.close()
    cssie7_out_file.close()

    # Creat zip file for download
    import subprocess
    PIPE = subprocess.PIPE
    zipfile = os.path.join(os.curdir, DOWNLOAD_DIR, ''.join([identifier, '.zip']))
    pd = subprocess.Popen(['/usr/bin/zip', '-r', '-j', zipfile, os.path.join(os.curdir, TMP_FILE_DIR, identifier)], stdout=PIPE, stderr=PIPE)
    stdout, stderr = pd.communicate()

    # Delete the files created so they don't take up space
    import shutil
    shutil.rmtree(os.path.join(os.curdir, TMP_FILE_DIR, identifier))

    return identifier


if __name__ == '__main__':
    app.run(host=app.config['LISTEN_ADDRESS'],port=app.config['LISTEN_PORT'])
