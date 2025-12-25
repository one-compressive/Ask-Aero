"""
Simple WSGI application without Django.
Displays GET and POST parameters.
Runs on localhost:8081
"""

def application(environ, start_response):
    """Simple WSGI application that displays GET and POST parameters"""

    # Parse GET parameters from QUERY_STRING
    get_params = {}
    if environ.get('QUERY_STRING'):
        query_string = environ['QUERY_STRING']
        for param in query_string.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                # URL decode
                from urllib.parse import unquote
                key = unquote(key)
                value = unquote(value)
                get_params[key] = value

    # Parse POST parameters from wsgi.input
    post_params = {}
    if environ.get('REQUEST_METHOD') == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        if request_body_size > 0:
            request_body = environ['wsgi.input'].read(request_body_size)
            # Decode bytes to string
            if isinstance(request_body, bytes):
                request_body = request_body.decode('utf-8')

            # Parse POST data
            for param in request_body.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    from urllib.parse import unquote
                    key = unquote(key)
                    value = unquote(value)
                    post_params[key] = value

    # Build HTML response
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>WSGI Parameters</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        .section {
            background-color: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .param-list {
            list-style-type: none;
            padding: 0;
        }
        .param-item {
            padding: 10px;
            margin: 5px 0;
            background-color: #f9f9f9;
            border-left: 3px solid #4CAF50;
        }
        .empty {
            color: #999;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1>WSGI Parameters Display</h1>

    <div class="section">
        <h2>GET Parameters</h2>
        <ul class="param-list">
"""

    if get_params:
        for key, value in get_params.items():
            html += f'            <li class="param-item"><strong>{key}:</strong> {value}</li>\n'
    else:
        html += '            <li class="param-item empty">No GET parameters</li>\n'

    html += """        </ul>
    </div>

    <div class="section">
        <h2>POST Parameters</h2>
        <ul class="param-list">
"""

    if post_params:
        for key, value in post_params.items():
            html += f'            <li class="param-item"><strong>{key}:</strong> {value}</li>\n'
    else:
        html += '            <li class="param-item empty">No POST parameters</li>\n'

    html += """        </ul>
    </div>

    <div class="section">
        <h2>Test Forms</h2>
        <form method="GET" action="">
            <h3>GET Request</h3>
            <input type="text" name="get_param1" placeholder="Parameter 1" value="">
            <input type="text" name="get_param2" placeholder="Parameter 2" value="">
            <button type="submit">Send GET</button>
        </form>

        <form method="POST" action="">
            <h3>POST Request</h3>
            <input type="text" name="post_param1" placeholder="Parameter 1" value="">
            <input type="text" name="post_param2" placeholder="Parameter 2" value="">
            <button type="submit">Send POST</button>
        </form>
    </div>
</body>
</html>"""

    # Set response headers
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    start_response(status, headers)
    return [html.encode('utf-8')]
