from flask import Flask, request, redirect, url_for, session
from flask_session import Session  # server-side sessions
import subprocess
import random
import os


# Configure Flask app
app = Flask(__name__)
app.secret_key = 'any secret string'

# Configure server-side session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

MENU = {
    "Silo Doors": {
        "Open Doors": "Opening Silo Doors...\n...ERROR: Operation failed. SYSTEM CORRUPTED!",
        "Close Doors": "Closing Silo Doors...\n...ERROR: Operation failed. SYSTEM CORRUPTED!",
        "Door Status": "Checking Door Status...\n...ERROR: Operation failed. SYSTEM CORRUPTED!"
    },
    "Security System": {
        "Activate System": "Activating Security System...\n...ERROR: Operation failed. SYSTEM CORRUPTED!",
        "Deactivate System": "Deactivating Security System...\n...ERROR: Operation failed. SYSTEM CORRUPTED!",
        "System Status": "Checking Security System Status...\n...ERROR: Operation failed. SYSTEM CORRUPTED!",
    },
    "Maintenance": {
        "Perform Routine Maintenance": "Performing Routine Maintenance...\n...ERROR: Operation failed. SYSTEM CORRUPTED!",
        "System Diagnostics": "Running System Diagnostics...\n...ERROR: Operation failed. SYSTEM CORRUPTED!",
        "Help": """
        Ah ah ah, you didn't say the magic word. 
        Memory Dump: [73, 110, 105, 116, 105, 97, 116, 105, 110, 103, 32, 115, 101, 99, 117, 114, 105, 116, 121, 32, 112, 114, 111, 116, 111, 99, 111, 108, 46, 46, 46, 32, 82, 101, 109, 98, 101, 114, 44, 32, 39, 112, 105, 112, 39, 32, 105, 115, 32, 116, 104, 101, 32, 98, 111, 121, 32, 102, 111, 114, 32, 39, 108, 105, 102, 101, 39, 46, 46, 46]
        """
    },
    "Missile Controls": {
        "Enter Key": "Please enter launch key:"
    }
}

hint_messages = [
    "System malfunction. Unexpected error at address 0x7f8b86d3. Pip... Err...",
    "Terminal failure. Code - 0x4c494645. Memory dump: [86, 97, 117, 108, 116, 101, 99, 104, 32, 115, 101, 99, 117, 114, 105, 116, 121, 32, 101, 110, 104, 97, 110, 99, 101, 109, 101, 110, 116, 32, 112, 114, 111, 99, 101, 100, 117, 114, 101, 32, 105, 110, 105, 116, 105, 97, 116, 101, 100...]",
    "Error 404: 'pipboy' object not found.",
    "Caution! Password protection active. Remember: 'life' is key...",
    "Exception! Address <'vault'> not found in memory.",
    "Terminal needs valid credentials. Run 'Enter' for user authentication.",
    "Terminal failure. Code - 0xD3FC0N31. Memory dump: [73, 110, 105, 116, 105, 97, 116, 105, 110, 103, 32, 115, 101, 99, 117, 114, 105, 116, 121, 32, 112, 114, 111, 116, 111, 99, 111, 108, 46, 46, 46, 32, 82, 101, 109, 101, 109, 98, 101, 114, 44, 32, 39, 112, 105, 112, 39, 32, 105, 115, 32, 116, 104, 101, 32, 98, 111, 121, 32, 102, 111, 114, 32, 39, 108, 105, 102, 101, 39, 46, 46, 46]",
    "Error 421: '/login' not found",
    "password format failure = ******#****"
]


# The secret password
password = "Death is a preferable alternative to communism"
flag = "flag{584d0218c9c70bfebb5416967f5a35a1}"


def render_menu(menu):
    options = ['0: Back'] if menu != MENU else []
    options.extend(f"{i}: {option}" for i, option in enumerate(menu, start=1) if option != "Missile Controls")
    return '\n'.join(options)


@app.route('/', methods=['GET', 'POST'])
def landing():
    menu_stack = session.get('menu_stack', [MENU])
    current_menu = menu_stack[-1]

    if request.method == 'POST':
        command = request.form['command']

        if command == '0':
            menu_stack = [MENU]
            session['menu_stack'] = menu_stack
            return render_landing_page(render_menu(menu_stack[-1]))
        elif command.lower() == 'missile controls':
            menu_stack.append(MENU['Missile Controls'])
            session['menu_stack'] = menu_stack
            return render_landing_page(render_menu(menu_stack[-1]))
        elif command == password and menu_stack[-1] == MENU['Missile Controls']:
            return render_landing_page(flag)
        else:
            try:
                selected_option = list(current_menu.keys())[int(command) - 1]
                if isinstance(current_menu[selected_option], dict):
                    menu_stack.append(current_menu[selected_option])
                    session['menu_stack'] = menu_stack
                    return render_landing_page(render_menu(menu_stack[-1]))
                else:
                    return render_landing_page(current_menu[selected_option])
            except (IndexError, ValueError):
                hint_message = random.choice(hint_messages)
                return render_landing_page(f"Invalid command!\n{hint_message}\n\n" + render_menu(current_menu))

    return render_landing_page(render_menu(current_menu))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'pipboy4life':
            session['authenticated'] = True
            return redirect(url_for('terminal'))
        else:
            return render_login_page(error=True)

    return render_login_page()


@app.route('/terminal', methods=['GET', 'POST'])
def terminal():
    if not session.get('authenticated', False):
        return redirect(url_for('login'))

    os.chdir('/app/data')  # change current working directory to /app/data

    if request.method == 'POST':
        command = request.form['command']
        try:
            result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode()
        except subprocess.CalledProcessError as e:
            result = str(e)
        return render_terminal_page(result=result)

    return render_terminal_page()


def render_landing_page(message=''):
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Vault-Tec Terminal</title>
        <style>
            body {{
                background-color: black;
                color: lime;
                font-family: 'Courier New', monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }}
            #command {{
                background-color: black;
                color: lime;
                border: 2px solid lime;
                width: 85%;
                height: 2em;
                padding: 5px;
            }}
            pre {{
                color: white;
            }}
        </style>
        <!-- SGludDogTG9vayBmb3Igc2VjcmV0IG1lbnUgb3B0aW9ucw== -->
        <script>
            document.addEventListener("DOMContentLoaded", function() {{
                var input = document.getElementById("command");
                input.addEventListener("keyup", function(event) {{
                    if (event.keyCode === 13) {{
                        event.preventDefault();
                        document.getElementById("landing-form").submit();
                    }}
                }});
            }});
        </script>
    </head>
    <body>
        <h1>Vault-Tec Missile Silo Terminal</h1>
        <h3>Silo Status: ERR-0R-404</h3>
        <pre>{message}</pre>
        <form id="landing-form" method=post>
          ><input id="command" type=text name=command>
        </form>
    </body>
    </html>
    '''


def render_login_page(error=False):
    error_msg = "<p>Incorrect password, please try again.</p>" if error else ""
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Vault-Tec Terminal - Login</title>
        <style>
            body {{
                background-color: black;
                color: lime;
                font-family: 'Courier New', monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }}
            .input-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 80%;
            }}
            input {{
                background-color: black;
                color: lime;
                border: 2px solid lime;
                width: 100%;
                height: 2em;
                margin-bottom: 10px;
                padding: 5px;
            }}
            p {{
                color: red;
            }}
        </style>
    </head>
    <body>
        <h1>Vault-Tec Secure Terminal</h1>
        <h2>Enter your password</h2>
        <form method=post>
          <div class="input-container">
            <input type=password name=password>
            <input type=submit value=Enter>
          </div>
        </form>
        {error_msg}
    </body>
    </html>
    '''


def render_terminal_page(result=''):
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Vault-Tec Terminal</title>
        <style>
            body {{
                background-color: black;
                color: lime;
                font-family: 'Courier New', monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }}
            #command {{
                background-color: black;
                color: lime;
                border: 2px solid lime;
                width: 85%;
                height: 2em;
                padding: 5px;
            }}
            pre {{
                color: white;
            }}
        </style>
        <script>
            document.addEventListener("DOMContentLoaded", function() {{
                var input = document.getElementById("command");
                input.addEventListener("keyup", function(event) {{
                    if (event.keyCode === 13) {{
                        event.preventDefault();
                        document.getElementById("terminal-form").submit();
                    }}
                }});
            }});
        </script>
    </head>
    <body>
        <h1>Vault-Tec Secure Terminal</h1>
        <pre>{result}</pre>
        <form id="terminal-form" method=post>
          ><input id="command" type=text name=command>
        </form>
    </body>
    </html>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,  debug=True)
