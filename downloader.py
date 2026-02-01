import requests
from flask import Flask, render_template, send_from_directory, request,redirect,url_for
from pathlib import Path
import threading
import shutil
from pathlib import Path

file_size = 0
dowwnload_speed = 0

def download_file(link, speed, filename):
    global filenames
    global file_size
    global dowwnload_speed
    file_link = link
    dowwnload_speed = int(speed)
    file_name = filename
    file = requests.get(file_link, stream=True)

    sizee = 1000000*dowwnload_speed
    file_size = int(file.headers['Content-Length'])/sizee

    download_file = open(file_name, 'wb')
    temp = dowwnload_speed
    for chunk in file.iter_content(sizee):
        download_file.write(chunk)
        
        print('\r%d/%0.2f' %(dowwnload_speed, file_size), flush=True, end='')
        dowwnload_speed+= temp
    filenames.append(file_name)
    dowwnload_speed = 0
    file_path = Path.cwd()/file_name
    new_path = Path.cwd()/'..'/'drive'/'MyDrive'/file_name

    shutil.move(file_path, new_path)
    
app = Flask(__name__, static_url_path='/')

filenames = []


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        thread_obj = threading.Thread(target=download_file, args=(request.form['link'],request.form['speed'],request.form['filename']))
        thread_obj.start()
    return render_template('home.html', filenames = filenames)

@app.route('/download/<name>')
def download(name):
    return send_from_directory(directory=Path.cwd(),path=name,as_attachment=True)

@app.route('/progress')
def progress():
    return render_template('progress.html', current = dowwnload_speed, total = file_size)

if __name__=='__main__':
    app.run(port=5000)