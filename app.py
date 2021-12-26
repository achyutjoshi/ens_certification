from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image, ImageFont, ImageDraw
import uuid

app = Flask(__name__)

MEDIA_FOLDER = 'images'

def create_image(generate_id, eth_name, block_id, txn_id):
    print(f'Starting for {generate_id}')
    my_image = Image.open("Letter - 1.png")
    width, height = my_image.size
    image_editable = ImageDraw.Draw(my_image)

    ## Name
    title_font = ImageFont.truetype('Overpass/static/Overpass-Bold.ttf', 28)
    title_text = eth_name
    w, h = image_editable.textsize(title_text, font=title_font)
    image_editable.text(((width - w) / 2, 255), title_text, (0, 0, 0), font=title_font)

    ## Block
    other_font = ImageFont.truetype('Overpass/static/Overpass-Regular.ttf', 16)
    block_text = str(block_id)
    image_editable.text((76, 458), block_text, (75, 75, 75), font=other_font)

    ## TXN ID
    other_font = ImageFont.truetype('Overpass/static/Overpass-Regular.ttf', 16)
    txn = txn_id
    image_editable.text((76, 510), txn, (75, 75, 75), font=other_font)
    output_name = 'result_' + generate_id + '.png'
    output_path = MEDIA_FOLDER + '/' + output_name
    my_image.save(output_path)
    print(f'Ended for {generate_id}')
    return output_name



@app.route('/')
def home():
    return render_template("front.html")


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    ens_name = request.form.get('ens_name')
    block_id = request.form.get('block_id')
    txn_id = request.form.get('txn_id')
    uid = str(uuid.uuid4())
    img_src = create_image(uid, ens_name, block_id, txn_id)
    return send_from_directory(MEDIA_FOLDER, img_src, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
