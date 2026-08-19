from flask import Flask
app= Flask(__name__)

@app.route('/')
def hello():
    return "Hello, flask~!!!"

@app.route('/users')
def get_users():
    return 'This is all user list'

@app.route('/users', methods=['POST'])
def post_users():
    return 'POST user!!'

from flask import request
@app.route('/boards', methods=['GET','POST'])
def board():
    if request.method=='GET':
        return 'board GET request'
    elif request.method=='POST':
        return 'board POST request'

@app.route('/test', methods=['GET'])
def get_test():
    name= request.args.get('name')
    message= request.args.get('msg')
    return f"{name}:{message}"

@app.route('/test', methods=['POST'])
def post_test():
    name= request.form.get('name')
    message= request.form.get('msg')
    return f"{name} <br> {message}"

@app.route('/notes', methods=['GET'])
def get_all_notes():
    return "all note data"

@app.route('/notes/<no>', methods=['GET'])
def get_note(no):
    return f"note {no}번"

@app.route('/notes2/<no>', methods=['GET'])
def get_note2(no):
    title= request.args.get('title')
    return f"note {no}번 - {title}"
    
@app.route('/notes2/<title>', methods=['POST'])
def post_note(title):
    message= request.form.get('msg')
    return f"{title} ~ {message}"

from flask import render_template
@app.route('/html')
def html():
    return render_template('note1.html')

#----------------------------------------------------------------------------
# Create
@app.route('/posts', methods=['POST'])
def save_data():
    title= request.form.get('title')
    return f"{title}: POST!!!♡"

# Read
@app.route('/posts', methods=['GET'])
def all_data():
    return f"all data get~*&*&*"

@app.route('/posts/<no>', methods=['GET'])
def get_data(no):
    return f"{no}번 data get^^"

# Update
@app.route('/posts/<no>', methods=['PUT'])
def update_data(no):
    return f"{no}번 data update%%"

# Delete
@app.route('/posts/<no>', methods=['DELETE'])
def delete_data(no):
    return f"{no}번 data delete **('ㅅ')**"

#----------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)