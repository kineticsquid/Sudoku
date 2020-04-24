"""
Deployment and debugging of this thing is not straight forward. It uses an environment variable URL_ROOT_KEY.
URL_ROOT_KEY can be used when deploying at runtime to deploy to something other and '/'. E.g.
'cloud.ibm.com/url_root/sudoku.

URL_ROOT_KEY is not needed when running the python script or when running the image locally. Use it when defining
a 'path' value for the ingress YAML that is not '/'. It's value needs to match what is specified for the ingress
path. URL_ROOT_KEY is also used in generating HTML from the Flask templates.

This goes with a GoDaddy domain name and CNAME entry. Subdomain sudoku.johnkellerman.org maps to https://sudoku-564793-074b55ec662880a9b91b986213323a0b-0000.us-east.containers.appdomain.cloud.

Puzzle URL is http://sudoku.johnkellerman.org/sudoku

"""
import os
from flask import Flask, request, render_template, Response, url_for
import re
import json
import solvePuzzle
import logging
import sys
import time
import uuid
import generateImage

app = Flask(__name__)

MATRIX_SIZE = 9
SUDOKU_DEBUG = 'SUDOKU_DEBUG'
URL_ROOT_KEY = 'URL_ROOT'
os.environ[SUDOKU_DEBUG] = 'Y'

url_root = os.environ.get(URL_ROOT_KEY, None)
if url_root is None:
    url_root = ''


"""
Method to define and return a logger for logging
"""


def get_my_logger():
    logger = logging.getLogger('My Logger')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(message)s', "%H:%M:%S")
    ch.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def extractMatrix(form):
    matrix_string = form.get('matrix-string', None)
    if matrix_string is not None:
        matrix = createInputMatrixFromString(matrix_string)
    else:
        matrix = []
        for row in range(0, 9):
            new_row = []
            value = 0
            for column in range(0, 9):
                fieldname = 'matrix%s%s' % (row, column)
                value = form.get(fieldname)
                if len(value) == 0:
                    new_row.append(0)
                else:
                    new_row.append(int(value))
            matrix.append(new_row)
    return matrix


def createInputMatrixFromString(matrix_string):
    matrix = []
    digit_re = re.compile('\d')
    results = digit_re.findall(matrix_string)
    new_row = []
    for result in results:
        new_row.append(int(result))
        if len(new_row) == MATRIX_SIZE:
            matrix.append(new_row)
            new_row = []
    return matrix

def getImageUrl(image_filename):
    image_url = '%s%s' % (request.host_url, image_filename)
    return image_url


@app.before_request
def do_something_whenever_a_request_comes_in():
    url = request.url
    if os.environ[SUDOKU_DEBUG] == 'Y':
        logger.info("Sudoku request: %s" % url)
        logger.info('Environ:\t%s' % request.environ)
        logger.info('Path:\t%s' % request.path)
        logger.info('Full_path:\t%s' % request.full_path)
        logger.info('Script_root:\t%s' % request.script_root)
        logger.info('Url:\t%s' % request.url)
        logger.info('Base_url:\t%s' % request.base_url)
        logger.info('Url_root:\t%s' % request.url_root)
        logger.info('Scheme:\t%s' % request.scheme)

@app.after_request
def apply_headers(response):
    # These are to fix low severity vulnerabilities identified by AppScan
    # in a dynamic scan
    response.headers['Content-Security-Policy'] = "object-src 'none'; script-src 'strict-dynamic'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


@app.errorhandler(Exception)
def handle_bad_request(e):
    logger.error('Error: %s' % str(e))
    return render_template('blank.html', message=str(e), title='Error!', url_root=url_root)


@app.route('/')
def welcomeToMyapp():
    return render_template('index.html', url_root=url_root)


@app.route('/echo', methods=['GET', 'POST'])
def echo():
    url = request.url
    output = 'URL: %s\n\n' % url
    form = request.form
    for key in form.keys():
        output = '%s\n%s - %s' % (output, key, form.get(key))
    return render_template('blank.html', message=str(output), title='Echo Input',
                           url_root=url_root)


@app.route('/printenv')
def printenv():
    output = 'Environment Variables:'
    for key in os.environ.keys():
        output = '%s\n%s - %s' % (output, key, os.environ.get(key))
    return render_template('blank.html', message=str(output), title='Environment Variables',
                           url_root=url_root)


@app.route('/debug')
def debug():
    os.environ[SUDOKU_DEBUG] = 'Y'
    return render_template('blank.html', message=str('Debug on'), title='Debug on',
                           url_root=url_root)


@app.route('/nodebug')
def nodebug():
    os.environ[SUDOKU_DEBUG] = 'N'
    return render_template('blank.html', message=str('Debug off'), title='Debug off',
                           url_root=url_root)


@app.route('/mobile')
def mobileWelcome():
    return render_template('mobile.html', url_root=url_root)


@app.route('/build')
def build():
    return app.send_static_file('build.txt')

@app.route('/createInputMatrix')
def createInputMatrix():
    queryParms = request.args
    inputString = queryParms.get('inputString')
    if inputString is not None:
        matrix = createInputMatrixFromString(inputString)
        if len(matrix) > 0:
            return Response(json.dumps(matrix), status=200, mimetype='application/json')
    # otherwise error condition
    error_content = {'Error': 'Missing or invalid input matrix'}
    return Response(json.dumps(error_content), status=400, mimetype='application/json')


@app.route('/getSolution', methods=['POST'])
def getSolution():
    payload = request.json
    inputMatrix = payload.get('inputMatrix')
    if inputMatrix is not None:
        try:
            puzzle = solvePuzzle.SudokuPuzzle(9)
            puzzle.set_inputs(inputMatrix)
            puzzle.compute_solution()
            solution_matrix = puzzle.values
            if len(solution_matrix) > 0:
                return Response(json.dumps(solution_matrix), status=200, mimetype='application/json')
            else:
                # otherwise error condition
                error_content = {'Error': 'Invalid or unsolvable input matrix'}
                return Response(json.dumps(error_content), status=400, mimetype='application/json')
        except Exception as e:
            error_content = {'Error': 'Invalid or unsolvable input matrix'}
            return Response(json.dumps(error_content), status=400, mimetype='application/json')
    else:
        error_content = {'Error': 'Invalid or unsolvable input matrix'}
        return Response(json.dumps(error_content), status=400, mimetype='application/json')

@app.route('/getImage', methods=['POST'])
def getImage():
    payload = request.json
    solution_matrix = payload.get('inputMatrix')
    if solution_matrix is not None:
        try:
            filename = str(uuid.uuid1())
            fullpath = app.static_folder + '/images/solutions/%s.png' % filename
            generateImage.generate(solution_matrix, fullpath)
            image_url = url_for('static', filename='images/solutions/%s.png' % filename)
            return Response(json.dumps({'imageURL' : image_url}), status=200, mimetype='application/json')

        except Exception as e:
            error_content = {'Error': 'Internal error generating solution image.'}
            return Response(json.dumps(error_content), status=500, mimetype='application/json')
    else:
        error_content = {'Error': 'Missing solution matrix input \'inputMatrix\'.'}
        return Response(json.dumps(error_content), status=400, mimetype='application/json')

@app.route('/solve', methods=['POST'])
def solve():
    form = request.form
    input_matrix = extractMatrix(form)
    if len(input_matrix) == 0:
        return render_template('blank.html', message="Missing or invalid input matrix",
                               title='Error!')
    if os.environ[SUDOKU_DEBUG] == 'Y':
        logger.info("input dictionary:")
        logger.info(json.dumps(input_matrix))
    puzzle = solvePuzzle.SudokuPuzzle(9)
    puzzle.set_inputs(input_matrix)
    puzzle.compute_solution()
    solution_matrix = puzzle.values
    template_values = {}
    for row in range(0, 9):
        for column in range(0, 9):
            fieldname = 'matrix%s%s' % (row, column)
            template_values[fieldname] = solution_matrix[row][column]
    template_values['url_root'] = url_root
    return render_template('index.html', **template_values)


port = os.getenv('PORT', '5010')

if __name__ == "__main__":
    logger = get_my_logger()
    logger.info('Starting %s....' % sys.argv[0])
    logger.info('Build: %s' % time.ctime(os.path.getmtime(sys.argv[0])))
    logger.info('Python: ' + sys.version)
    logger.info('Environment Variables:')
    for key in os.environ.keys():
        logger.info('%s:\t%s' % (key, os.environ.get(key)))
    logger.info('App static folder: %s' % app.static_folder)
    app.run(host='0.0.0.0', port=int(port))
