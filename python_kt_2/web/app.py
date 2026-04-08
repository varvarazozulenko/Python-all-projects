from pathlib import Path
from flask import Flask, render_template, request
from .. import use_cases

app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/stats')
def stats():
    return render_template('stats.html')


@app.post('/stats')
def stats_process():
    try:
        pos = request.form.get('pos') == 'on'
        text_file = request.files.get('file')

        if not text_file or text_file.filename == '':
            return render_template('stats.html', error="Пожалуйста, выберите файл")

        if not text_file.filename.endswith('.txt'):
            return render_template('stats.html', error="Пожалуйста, загрузите файл в формате .txt")

        destination = Path() / 'python_kt_2' / 'corpus' / text_file.filename
        text_file.save(destination)

        text = destination.read_text(encoding='utf-8')

        result = use_cases.stats(text, pos)

        return render_template('stats.html', result=result)

    except Exception as e:
        return render_template('stats.html', error=f"Ошибка при обработке: {str(e)}")


@app.get('/top')
def top_words_page():
    return render_template('topwords.html')


@app.post('/top')
def top_words_process():
    try:
        text_file = request.files.get('file')
        normalize_mode = request.form.get('normalize_mode', 'stemming')

        if not text_file or text_file.filename == '':
            return render_template('topwords.html', error="Пожалуйста, выберите файл")

        if not text_file.filename.endswith('.txt'):
            return render_template('topwords.html', error="Пожалуйста, загрузите файл в формате .txt")

        destination = Path() / 'python_kt_2' / 'corpus' / text_file.filename
        text_file.save(destination)

        text = destination.read_text(encoding='utf-8')

        result = use_cases.top_words(text, normalize_mode)

        top_20 = result[:20]
        return render_template('topwords.html', result=top_20)

    except Exception as e:
        return render_template('topwords.html', error=f"Ошибка при обработке: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)