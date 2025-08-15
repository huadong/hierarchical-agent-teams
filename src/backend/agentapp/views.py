import json
import os.path as path
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage

from django.shortcuts import HttpResponse
from django.http import FileResponse, StreamingHttpResponse
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from agent.graph import app

def cros(response: HttpResponse):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, DELETE"
    response.headers["Access-Control-Max-Age"] = "3600"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Create your views here.
def index(request: WSGIRequest):
    # Render the HTML template index.html with the data in the context variable.
    return HttpResponse(json.dumps('test'), content_type='application/json')


def question(request: WSGIRequest):
    if request.method == 'OPTIONS' or request.method == 'GET':
        return cros(HttpResponse(''))
    input = json.loads(request.body.decode('utf-8'))
    
    inputs = {
        "messages": [
            ("user", input["question"])
        ],
    }
    def generate():
        def composite_messages(messages):
            text = ''
            for message in messages:
                if isinstance(message, str):
                    text += message
                elif isinstance(message, HumanMessage):
                    text += message.content
                elif isinstance(message, ToolMessage):
                    try:
                        content = json.loads(message.content)
                        result = '\n\n'.join([f'{k}: {v}' for r in content['results'] for k,v in r.items()])
                        text += f"Tool: {message.name}\n\nQuery: {content['query']}\n\nResults:\n\n{result}\n\n"
                    except:
                        text += f"Tool: {message.name}\n\nContent: {message.content}\n\n"
                elif isinstance(message, AIMessage):
                    text += message.content
                else:
                    raise ValueError(f"Unknown message type: {type(message)}")
            return text

        final_value = None
        for output in app.stream(inputs, {"recursion_limit": 150}, subgraphs = True):
            namespace = output[0]
            node = output[1]
            for key, value in node.items():
                # value contains messages
                if "messages" in value or "next" in value:
                    line = {
                        "namespace": "/".join([ n.split(":")[0] for n in namespace]),
                        "node": key,
                        "value": composite_messages(value["messages"]) if "messages" in value else value["next"],
                    }
                    try:
                        text = json.dumps(line) + "\n"
                        yield text
                    except Exception:
                        pass

    response = StreamingHttpResponse(generate(), content_type='application/json')
    response['X-Accel-Buffering'] = 'no'
    return cros(response)