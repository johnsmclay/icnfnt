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
#app.config.from_envvar('ICNFNT_CONFIG')
app.config.from_object(__name__)
app.config['DEBUG'] = True

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

    # Beginning of glyph unicde range
    GLYPHS_CODE_START = 0xf021
    glyphcode = GLYPHS_CODE_START

    # Fire up the reference font
    f = fontforge.open('fonts/fontawesome-webfont.ttf')
    f.encoding = 'UnicodeFull'

    # Set up the new font shell
    nf = fontforge.font()
    nf.encoding = 'UnicodeFull'
    nf.fontname = name
    nf.fullname = name
    nf.familyname = name
    nf.ascent = 850
    nf.em = 1792
    nf.descent = 256
    nf.gasp =  ((65535, ('gridfit', 'antialias', 'symmetric-smoothing', 'gridfit+smoothing')),)
    nf.gasp_version = 1
    nf.hhea_descent = -34
    nf.hhea_linegap = 0
    nf.os2_codepages =  (1, 0)
    nf.os2_fstype = 4
    nf.os2_panose =  (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    nf.os2_strikeypos = 1075
    nf.os2_strikeysize = 90
    nf.os2_subyoff = 134
    nf.os2_subysize = 1075
    nf.os2_supyoff = 627
    nf.os2_supysize = 1075
    nf.os2_typolinegap = 0
    nf.weight =  'Book'

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

    # Add each glyph to the new font & related style + html files
    for character in req_chars:

        # If there is no SVG file set in the file attribute, snag the glyph from the reference font
        if not character["file"]:
            
            # Find the glyph and copy it
            f.selection.select(("more", "unicode", None), ''.join(['uniF', str(character['uni'])]))
            f.copy()
            
            # Create a new glyph at the next generated unicode address, paste the outlines, re-name it
            nf.selection.select(("unicode",), glyphcode)
            nf.paste()
            nf[glyphcode].glyphname = character["name"]
            
            # Clear the selections
            f.selection.none()
            nf.selection.none()
        
        # Otherwise get the outlines from the SVG and add-away
        else:
            # Build the SVG path
            file_path = os.path.join('svg/', character['file'])
            
            # Make a new glyph at the next generated unicode address
            g = nf.createChar(glyphcode, character['name'])
            
            # Slam the SVG outlines into the glyph
            g.importOutlines(file_path)

            # Tweak the glyph slightly
            g.left_side_bearing = 15
            g.right_side_bearing = 15
        
        # Make the newly created glyph available to generate the rest of the files
        ng = nf[glyphcode]

        # Increment next glyph unicode address
        glyphcode += 1

        # Write out the supplementary files
        html_out_file.write(''.join(['<tr><td><i class="icon-', str(ng.glyphname), '"></i></td><td>.icon-', str(ng.glyphname), '</td></tr>']))
        less_out_file.write(''.join(['.icon-', str(ng.glyphname), ':before', "\t\t", '{ content: "', str(hex(ng.unicode)).replace("0xf","\\f"), '"; }', "\n"]))
        lessie7_out_file.write(''.join(['.icon-', str(ng.glyphname), "\t\t", "{ .ie7icon('", str(hex(ng.unicode)).replace("0xf","&#xf"), ";'); }", "\n"]))
        sass_out_file.write(''.join(['.icon-', str(ng.glyphname), ':before', "\n\t", 'content: "', str(hex(ng.unicode)).replace("0xf","\\f"), '"', "\n\n"]))
        scss_out_file.write(''.join(['.icon-', str(ng.glyphname), ':before', "\t\t", '{ content: "', str(hex(ng.unicode)).replace("0xf","\\f"), '"; }', "\n"]))
        css_out_file.write(''.join(['.icon-', str(ng.glyphname), ':before', "\t\t", '{ content: "', str(hex(ng.unicode)).replace("0xf","\\f"), '"; }', "\n"]))
        cssie7_out_file.write(''.join(['.icon-', str(ng.glyphname), " { *zoom: expression( this.runtimeStyle['zoom'] = '1', this.innerHTML = '", str(hex(ng.unicode)).replace("0xe","&#xf"), ";&nbsp;'); }", "\n"]))

    # Kick out the various font files
    filetypes = [   'ttf',
                    'eot',
                    'woff',
                ]

    # Actually generate each of the font types
    for filetype in filetypes:
            nf.generate(os.path.join(os.curdir, TMP_FILE_DIR, identifier, ''.join([name, '-webfont.', filetype])))
    nf.close()
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
    #app.run(host=app.config['LISTEN_ADDRESS'],port=app.config['LISTEN_PORT'])
    app.run()
