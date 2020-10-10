#deep learning libraries

#web frameworks
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
import uvicorn
import joblib
import fastai

import os
import sys
import base64 

app = Starlette()
# path = Path('')
# learner = load_learner(path)

pkl_filename = "joblib_model.pkl"
file = open(pkl_filename,'rb')
pickle_model = joblib.load(file)


@app.route("/upload", methods = ["POST"])
async def upload(request):
    data = await request.form()
    wav_file = await (data["file"])
    return predict_audio_from_bytes(wav_file)

@app.route("/classify-url", methods = ["GET"])
async def classify_url(request):
    bytes = await get_bytes(request.query_params["url"])
    return predict_audio_from_bytes(bytes)

def predict_audio_from_bytes(wav_file):
    resultado = pickle_model.predict(wav_file) 
    return HTMLResponse(
        """
        <html>
            <body>
                <p> Prediction: <b> %s </b> </p>
            </body>
        </html>
        """ %(resultado))
        
@app.route("/")
def form(request):
        return HTMLResponse(
            """
            <h1> Greenr </h1>
            <p> Is your picture of a dandelion or grass? </p>
            <form action="/upload" method = "post" enctype = "multipart/form-data">
                <u> Select picture to upload: </u> <br> <p>
                1. <input type="file" name="file"><br><p>
                2. <input type="submit" value="Upload">
            </form>
            <br>
            <br>
            <u> Submit picture URL </u>
            <form action = "/classify-url" method="get">
                1. <input type="url" name="url" size="60"><br><p>
                2. <input type="submit" value="Upload">
            </form>
            """)
        
@app.route("/form")
def redirect_to_homepage(request):
        return RedirectResponse("/")

@app.route("/identificar", methods = ["POST"])
async def identificar(request):
    wav = request.files['file']
    resultado = pickle_model.predict(wav) 
    return resultado
    # data = await request.form()
    # bytes = await (data["file"].read())
    # return predict_audio_from_bytes(bytes)

       
        
if __name__ == "__main__":
    if "serve" in sys.argv:
        port = int(os.environ.get("PORT", 8008)) 
        uvicorn.run(app, host = "0.0.0.0", port = port)
