
# coding: utf-8

# In[1]:


import WebData as wd


# In[137]:


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/settlement', methods=["GET"])
def get_settlement():
    try:
        date = request.args.get("date")
        df = wd.settlement(date)
        return df.to_json(orient="records")
        
    except:
        res = {"pythonError":traceback.format_exc()}
        return jsonify(res)
    
@app.route('/hoep', methods=["GET"])
def get_hoep():
    try:
        date = request.args.get("date")
        df = wd.hoep(date)
        return df.to_json(orient="records")
    
    except:
        res = {"pythonError":traceback.format_exc()}
        return jsonify(res)
    
@app.route('/gen', methods=["GET"])
def get_gen():
    try:
        date = request.args.get("date")
        df = wd.gen(date)
        return df.to_json(orient="records")
    
    except:
        res = {"pythonError":traceback.format_exc()}
        return jsonify(res)
    
@app.route('/weather', methods=["GET"])
def get_weather():
    try:
        month = request.args.get("date")
        df = wd.weather(month)
        return df.to_json(orient="records")
    
    except:
        res = {"pythonError":traceback.format_exc()}
        return jsonify(res)

@app.after_request
def addCORS(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Max-Age", "3600")
    response.headers.add("Access-Control-Request-Headers", "Content-Type")
    return response
    
@app.route('/shutdown', methods=["GET"])
def fn_shutdown():
    if request.method == "GET":
        request.environ.get('werkzeug.server.shutdown')()
        return "Server shutting down..."

app.run(port=9999)

