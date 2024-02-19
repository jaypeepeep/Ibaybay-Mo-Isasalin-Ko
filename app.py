from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
import LatinToBaybayin
import BaybayinToLatin
import BaybayinRecognizer
from PIL import Image
import base64
import os
import centerCanvas, bottomCanvas, topCanvas


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transliterate/latin-to-baybayin', methods=['POST'])
def translit_from_latin_to_baybayin():
    data = request.get_json()

    if 'input' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    input_str = data['input']

    converter = LatinToBaybayin.LatinToBaybayin()
    result = converter.process_input(input_str)
    if converter.state == converter.state == "dead" or converter.state == "consonant" or converter.state == "digraph": # If last input is not in a final state
        result = "Input not available in Baybayin"
    elif converter.state == "final_consonant": # If last input is a final consonant
        result = result[:-1]
    elif converter.state == "final_digraph": # If last input is a final digraph
            result = result[:-2]

    return jsonify({'result': result})

syllabic = ["BA", "CA", "DA", "FA", "GA", "HA", "JA", "KA", "LA", "MA", "NA", "NGA", "PA", "QA", "RA", "SA", "TA", "VA", "WA", "XA", "YA", "ZA"]

@app.route('/api/transliterate/baybayin-to-latin', methods=['POST'])
def translit_from_baybayin_to_latin():
    data = request.get_json()

    if 'charInput' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    
    char_input = data['charInput']

    input_str = char_input
    # Replace '||' with a space
    input_str = input_str.replace('||', ' ')

    converter = BaybayinToLatin.BaybayinToLatin()
    result = converter.process_input(input_str, syllabic)
    if converter.state == "start": # If input is only in a start state
        result = "Enter a character"
    elif converter.state == "dead": # If last input is not in a final state
        result = "Input not available in Baybayin"
    
    return jsonify({'result': result})




@app.route('/about') 
def about():
    return render_template('about.html')

@app.route('/practice') 
def practice():
    return render_template('practice.html')

if not os.path.exists('img'):
    os.makedirs('img')

@app.route('/api/runpy', methods=['POST'])
def runpy():
    data = request.get_json()
    
    center = data['centerValue']
    top = data['topValue']
    bottom = data['bottomValue']
    
    print(center)
    print(top)
    print(bottom)
    
    syllabic = ["BA", "CA", "DA", "FA", "GA", "HA", "JA", "KA", "LA", "MA", "NA", "NGA", "PA", "QA", "RA", "SA", "TA", "VA", "WA", "XA", "YA", "ZA"]
    vowel = ["A", "E or I", "O or U"]

    # Initialize the Pushdown Automaton
    automata = BaybayinRecognizer.BaybayinRecognizer(syllabic, vowel)

    # Example 1∈
    automata.process_input("centerCanvas", center)
    automata.process_input("topCanvas", top)
    automata.process_input("bottomCanvas", bottom)
    result = automata.get_result()
    print(f"Output: {result}")
    
    # Return the concatenated result in a single JSON response
    return jsonify({'result': result})

@app.route('/api/capture_canvas', methods=['POST'])
def capture_canvas():
    data = request.get_json()

    if 'canvasId' not in data or 'dataURL' not in data:
        return jsonify({'success': False, 'error': 'Invalid request'}), 400

    canvas_id = data['canvasId']
    data_url = data['dataURL']

    # Assuming you have a function to convert base64 data URL to an image, modify accordingly
    image = convert_data_url_to_image(data_url)

    # Remove the alpha channel (transparency) if present
    image = remove_alpha_channel(image)

    # Resize the image to 28x28
    resized_image = resize_image(image, (28, 28))

    # Save the resized image to the 'img' directory with an incrementing file name
    image_filename = f'img/{canvas_id}_output.jpg'
    resized_image.save(image_filename)

    # Initialize the Pushdown Automaton
    vowel = ["A", "E", "I", "O", "U"]
    
    automata = BaybayinRecognizer.BaybayinRecognizer(syllabic, vowel)
    
    if(canvas_id == "centerCanvas"):
        result = centerCanvas.defineCenter(f'img/centerCanvas_output.jpg')
    if(canvas_id == "topCanvas"):
        result = topCanvas.defineTop(f'img/topCanvas_output.jpg')
    if(canvas_id == "bottomCanvas"):
        result = bottomCanvas.defineBottom(f'img/bottomCanvas_output.jpg')
    
    print(canvas_id + " " + result)

    # Return the concatenated result in a single JSON response
    return jsonify({'result': result, 'canvas_name': canvas_id})


def convert_data_url_to_image(data_url):
    # Remove the data URL prefix
    data_url = data_url.split(',')[1]

    # Decode base64 data
    image_data = BytesIO(base64.b64decode(data_url))

    # Use PIL to open the image stream
    image = Image.open(image_data)

    return image

def remove_alpha_channel(image):
    # Convert the image to RGB mode (removing alpha channel)
    return image.convert('RGB')

def resize_image(image, size):
    # Resize the image
    resized_image = image.resize(size)

    return resized_image


if __name__ == '__main__':
    app.run(debug=True)