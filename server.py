from flask import Flask, render_template, request, redirect, url_for,send_from_directory
import subprocess
import os
import webbrowser
app = Flask(__name__,static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extractImage', methods=['POST'])
def extract():
    # 调用 ExtractImageFromPdf.py 脚本
    subprocess.run(['python', 'ExtractImageFromPdf.py'])
    return redirect(url_for('index'))
    
@app.route('/extractText', methods=['POST'])
def text():
    # 调用 compare.py 脚本
    subprocess.run(['python', 'compare.py'])
    return redirect(url_for('index'))
 
 
@app.route('/OpenPdf', methods=['POST'])
def show_pdf():
    return send_from_directory(static_folder,'showpdf.html')   
        
@app.route('/paths.txt')
def get_paths():
    return send_from_directory(static_folder, 'paths.txt')
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)