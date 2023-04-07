import os
from flask import Flask, request, render_template, redirect
import re
import json
import solvePuzzle
import logging
import sys

app = Flask(__name__)

MATRIX_SIZE = 9
SUDOKU_DEBUG = 'SUDOKU_DEBUG'
os.environ[SUDOKU_DEBUG] = 'N'

logging.basicConfig(level=logging.INFO)

def log(log_message):
    if app is not None:
        app.logger.info(log_message)
    else:
        print(log_message)

def generate_template_values(input_matrix=None, solution_matrix=None):
    fields = {}
    for row in range(0, 9):
        for column in range(0, 9):
            style_field_name = 'style%s%s' % (row, column)
            digit_field_name = 'matrix%s%s' % (row, column)
            if (row < 3 or row > 5) and (column < 3 or column > 5) or (3 <= row <= 5) and (3 <= column <= 5):
                if solution_matrix is None:
                    fields[style_field_name] = "odd-input"
                else:
                    if input_matrix[row][column] == 0:
                        fields[style_field_name] = "odd-answer"
                    else:
                        fields[style_field_name] = "odd-input"
            else:
                if solution_matrix is None:
                    fields[style_field_name] = "even-input"
                else:
                    if input_matrix[row][column] == 0:
                        fields[style_field_name] = "even-answer"
                    else:
                        fields[style_field_name] = "even-input"   
            if solution_matrix is not None:
                fields[digit_field_name] = solution_matrix[row][column]
    return fields  

DEFAULT_STYLES = generate_template_values()         

"""
Method to define and return a logger for logging
"""


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
        log("Sudoku request: %s" % url)
        log('Environ:\t%s' % request.environ)
        log('Path:\t%s' % request.path)
        log('Full_path:\t%s' % request.full_path)
        log('Script_root:\t%s' % request.script_root)
        log('Url:\t%s' % request.url)
        log('Base_url:\t%s' % request.base_url)
        log('Url_root:\t%s' % request.url_root)
        log('Scheme:\t%s' % request.scheme)

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
    log('Error: %s' % str(e))
    return render_template('blank.html', message=str(e), title='Error!')


@app.route('/')
def welcomeToMyapp():
    return render_template('index.html', **DEFAULT_STYLES)


@app.route('/debug')
def debug():
    os.environ[SUDOKU_DEBUG] = 'Y'
    return render_template('blank.html', message=str('Debug on'), title='Debug on')


@app.route('/nodebug')
def nodebug():
    os.environ[SUDOKU_DEBUG] = 'N'
    return render_template('blank.html', message=str('Debug off'), title='Debug off')


@app.route('/build', methods=['GET', 'POST'])
def build():
    try:
        build_file = open('static/build.txt')
        build_stamp = build_file.readlines()[0]
        build_file.close()
    except FileNotFoundError:
        build_stamp = generate_build_stamp()
    results = 'Running %s %s.\nBuild %s.\nPython %s.' % (sys.argv[0], app.name, build_stamp, sys.version)
    return results

def generate_build_stamp():
    from datetime import date
    return 'Development build - %s' % date.today().strftime("%m/%d/%y")


@app.route('/solve', methods=['POST'])
def solve():
    form = request.form
    input_matrix = extractMatrix(form)
    if len(input_matrix) == 0:
        return render_template('blank.html', message="Missing or invalid input matrix",
                               title='Error!')
    if os.environ[SUDOKU_DEBUG] == 'Y':
        log("input dictionary:")
        log(json.dumps(input_matrix))
    puzzle = solvePuzzle.SudokuPuzzle(9)
    puzzle.set_inputs(input_matrix)
    puzzle.compute_solution()
    solution_matrix = puzzle.values
    template_values = generate_template_values(input_matrix=input_matrix, solution_matrix=solution_matrix)
    return render_template('index.html', **template_values)

@app.route('/clear', methods=['POST'])
def clear():
    return redirect('/')


log('Starting %s %s' % (sys.argv[0], app.name))
log('Python: ' + sys.version)
try:
    build_file = open('static/build.txt')
    build_stamp = build_file.readlines()[0]
    build_file.close()
except FileNotFoundError:
    from datetime import date
    build_stamp = generate_build_stamp()
log('Running build: %s' % build_stamp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))