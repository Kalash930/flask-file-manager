from flask import Flask, render_template, request, redirect, flash
import os

app = Flask(__name__)
app.secret_key = 'supersecret'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    filename = request.form['filename']
    content = request.form['content']
    if os.path.exists(filename):
        flash("File already exists.", "danger")
    else:
        try:
            with open(filename, 'w') as f:
                f.write(content)
            flash("File created successfully.", "success")
        except Exception as e:
            flash(str(e), "danger")
    return redirect('/')

@app.route('/read', methods=['POST'])
def read():
    filename = request.form['filename']
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
            return render_template('index.html', read_content=content)
        except Exception as e:
            flash(str(e), "danger")
    else:
        flash("File does not exist.", "danger")
    return redirect('/')

@app.route('/update', methods=['POST'])
def update():
    filename = request.form['filename']
    content = request.form['content']
    if os.path.exists(filename):
        try:
            with open(filename, 'a') as f:
                f.write("\n" + content)
            flash("File updated.", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        flash("File does not exist.", "danger")
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    filename = request.form['filename']
    if os.path.exists(filename):
        try:
            os.remove(filename)
            flash("File deleted.", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        flash("File not found.", "danger")
    return redirect('/')

@app.route('/list')
def list_files():
    files = [f for f in os.listdir() if os.path.isfile(f)]
    return render_template('index.html', files=files)

@app.route('/search', methods=['POST'])
def search():
    filename = request.form['filename']
    word = request.form['word']
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read()
            found = word in content
        return render_template('index.html', search_result=(word, found))
    else:
        flash("File does not exist.", "danger")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
