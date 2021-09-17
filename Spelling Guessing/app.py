import nltk


nltk.download('punkt')
from flask import Flask,request,jsonify,render_template
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize

nltk.download('gutenberg')
nltk.download('punkt')
tt = gutenberg.raw('bible-kjv.txt')

txt = word_tokenize(tt)


def correct1(word):
    # this will help me to split my word into left and right
    splits = []
    # len(word)+1 is used to take space
    for i in range(len(word) + 1):
        splits.append((word[:i], word[i:]))
    # this will delete my first value in right word
    deletes1 = []
    for L, R in splits:
        if R:
            deletes1.append((L + R[1:]))
    # this will swap first value and second value in Rigt word
    transpose = []
    for L, R in splits:
        if len(R) > 1:
            transpose.append((L + R[1] + R[0] + R[2:]))
    # this will replace replace value with letters  placed in every single place ,just for making combination
    replaces = []
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for L, R in splits:
        for c in letters:
            replaces.append((L + c + R[1:]))
    # insert value in  random moving letters placed in every single place ,just for making combination
    inserts = []
    for L, R in splits:
        for c in letters:
            inserts.append((L + c + R))

    cr = set(inserts + deletes1 + transpose + replaces + inserts)

    prob = {}
    for i in cr:
        prob[i] = txt.count(i) / len(txt)
    return prob


app=Flask(__name__)


def corr(wo):
    prob = correct1(wo)
    prob_words = []

    words = []
    output = []
    for word, probability in prob.items():
        words.append(word)
        prob_words.append(probability)
    for i in range(len(prob_words)):
        if prob_words[i] > 0:
            for j in range(len(words)):
                if i == j:
                    output.append(words[i])

    return output


# print(corr('sentenced'))

@app.route('/')
def correct():
    return render_template('correct2.html')


#     return 'hello'
# time.sleep(1)
@app.route('/', methods=['POST'])
# <form  action="{{ url_for('getvalue') }}" method="post">
# action is in html form used to get url from this form
def getvalue():
    val = request.form['name1']
    #     print(val)background-color:powderblue;
    cor = corr(str(val))

    return render_template('correct2.html', name=cor)


if __name__ == '__main__':
    app.run()
