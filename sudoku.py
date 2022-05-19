import os
from flask import Flask, request, render_template, Response
import re
import json
import solvePuzzle
import logging
import sys

app = Flask(__name__)

MATRIX_SIZE = 9
SUDOKU_DEBUG = 'SUDOKU_DEBUG'
os.environ[SUDOKU_DEBUG] = 'Y'

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
        print("Sudoku request: %s" % url)
        print('Environ:\t%s' % request.environ)
        print('Path:\t%s' % request.path)
        print('Full_path:\t%s' % request.full_path)
        print('Script_root:\t%s' % request.script_root)
        print('Url:\t%s' % request.url)
        print('Base_url:\t%s' % request.base_url)
        print('Url_root:\t%s' % request.url_root)
        print('Scheme:\t%s' % request.scheme)

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
    print('Error: %s' % str(e))
    return render_template('blank.html', message=str(e), title='Error!')


@app.route('/')
def welcomeToMyapp():
    return render_template('index.html')

@app.route('/2')
def welcomeToMyapp2():
    return render_template('index2.html')


@app.route('/echo', methods=['GET', 'POST'])
def echo():
    url = request.url
    output = 'URL: %s\n\n' % url
    form = request.form
    for key in form.keys():
        output = '%s\n%s - %s' % (output, key, form.get(key))
    return render_template('blank.html', message=str(output), title='Echo Input')

@app.route('/debug')
def debug():
    os.environ[SUDOKU_DEBUG] = 'Y'
    return render_template('blank.html', message=str('Debug on'), title='Debug on')


@app.route('/nodebug')
def nodebug():
    os.environ[SUDOKU_DEBUG] = 'N'
    return render_template('blank.html', message=str('Debug off'), title='Debug off')


@app.route('/mobile')
def mobileWelcome():
    return render_template('mobile.html')


@app.route('/build', methods=['GET', 'POST'])
def build():
    try:
        build_file = open('static/build.txt')
        build_stamp = build_file.readlines()[0]
        build_file.close()
    except FileNotFoundError:
        from datetime import date
        build_stamp = generate_build_stamp()
    results = 'Running %s %s.\nBuild %s.\nPython %s.' % (sys.argv[0], app.name, build_stamp, sys.version)
    return results

def generate_build_stamp():
    from datetime import date
    return 'Development build - %s' % date.today().strftime("%m/%d/%y")


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

@app.route('/solve', methods=['POST'])
def solve():
    form = request.form
    input_matrix = extractMatrix(form)
    if len(input_matrix) == 0:
        return render_template('blank.html', message="Missing or invalid input matrix",
                               title='Error!')
    if os.environ[SUDOKU_DEBUG] == 'Y':
        print("input dictionary:")
        print(json.dumps(input_matrix))
    puzzle = solvePuzzle.SudokuPuzzle(9)
    puzzle.set_inputs(input_matrix)
    puzzle.compute_solution()
    solution_matrix = puzzle.values
    template_values = {}
    for row in range(0, 9):
        for column in range(0, 9):
            fieldname = 'matrix%s%s' % (row, column)
            template_values[fieldname] = solution_matrix[row][column]
    return render_template('index.html', **template_values)


print('Starting %s %s' % (sys.argv[0], app.name))
print('Python: ' + sys.version)
try:
    build_file = open('static/build.txt')
    build_stamp = build_file.readlines()[0]
    build_file.close()
except FileNotFoundError:
    from datetime import date
    build_stamp = generate_build_stamp()
print('Running build: %s' % build_stamp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))