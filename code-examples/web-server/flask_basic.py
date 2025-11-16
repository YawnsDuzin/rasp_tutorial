#!/usr/bin/env python3
"""
기본 Flask 웹 서버
간단한 웹 페이지를 제공합니다.

설치:
pip install flask

실행:
python3 flask_basic.py

접속:
http://raspberrypi.local:5000
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>라즈베리파이 웹 서버</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f0f0f0;
            }
            h1 { color: #c51a4a; }
            .card {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🍓 라즈베리파이 웹 서버</h1>
            <p>Flask를 사용한 간단한 웹 애플리케이션입니다.</p>
            <ul>
                <li><a href="/">홈</a></li>
                <li><a href="/about">소개</a></li>
                <li><a href="/info">시스템 정보</a></li>
            </ul>
        </div>
    </body>
    </html>
    '''

@app.route('/about')
def about():
    return '''
    <h1>소개</h1>
    <p>이것은 라즈베리파이에서 실행되는 Flask 웹 서버입니다.</p>
    <a href="/">홈으로</a>
    '''

@app.route('/info')
def info():
    import platform
    import os

    info_text = f"""
    <h1>시스템 정보</h1>
    <ul>
        <li>시스템: {platform.system()}</li>
        <li>호스트명: {platform.node()}</li>
        <li>아키텍처: {platform.machine()}</li>
        <li>Python 버전: {platform.python_version()}</li>
    </ul>
    <a href="/">홈으로</a>
    """
    return info_text

if __name__ == '__main__':
    print("Flask 웹 서버 시작...")
    print("접속: http://raspberrypi.local:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
