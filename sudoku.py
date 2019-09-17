import os.path
from flask import Flask, request, render_template
import re
import json
import solvePuzzle

app = Flask(__name__)

SOLVER_FUNCTION_URL = 'https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/solve'
SOLUTION_IMAGE_DIR = 'static/solutions'
MATRIX_SIZE = 9


def extractMatrix(form):
    matrix = []
    matrix_string = form.get('matrix-string', None)
    if matrix_string is not None:
        digit_re = re.compile('\d')
        results = digit_re.findall(matrix_string)
        new_row = []
        for result in results:
            new_row.append(int(result))
            if len(new_row) == MATRIX_SIZE:
                matrix.append(new_row)
                new_row = []
    else:
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


def getImageUrl(image_filename):
    image_url = '%s%s' % (request.host_url, image_filename)
    return image_url


@app.before_request
def do_something_whenever_a_request_comes_in():
    url = request.url
    print("Sudoku request: %s" % url)

@app.errorhandler(Exception)
def handle_bad_request(e):
    return render_template('error.html', message=str(e))

@app.route('/')
def welcomeToMyapp():
    return render_template('index.html')


@app.route('/mobile')
def mobileWelcome():
    return render_template('mobile.html')


@app.route('/build')
def build():
    return app.send_static_file('build.txt')


@app.route("/solve", methods=['POST'])
def solve():
    form = request.form
    input_matrix = extractMatrix(form)
    if len(input_matrix) == 0:
        return render_template('error.html', message="Missing or invalid input matrix")
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


port = os.getenv('PORT', '5000')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
