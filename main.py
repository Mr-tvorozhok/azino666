from flask import Flask, request

app = Flask(__name__)


@app.route('/')
@app.route('/registred', methods=["GET", "POST"])
def registred():
    qwe = ''
    print(2)
    if request.method == "POST":
        print(1)
        qwe = request.form['query']
        print(3)
        print(qwe)
    with open('registred.html', 'r', encoding="utf-8") as html_stream:
        html = html_stream.read()
    dictt = {"temperature": "66364", "wind_speed": qwe}
    print(dictt)
    for replace in dictt:

        html = html.replace(f'{{{{ {replace} }}}}', dictt[replace])


    return html


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')