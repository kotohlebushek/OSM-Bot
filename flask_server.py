from flask import Flask, render_template
from database import get_all_markers

app = Flask(__name__)


@app.route('/map/<unique_id>')
def map_page(unique_id):
    markers = get_all_markers()
    marker_data = [{"id": m[0], "latitude": m[1], "longitude": m[2]} for m in markers]
    return render_template("map.html", unique_id=unique_id, markers=marker_data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
