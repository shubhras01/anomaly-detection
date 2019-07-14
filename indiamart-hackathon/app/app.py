import os
import StringIO
import base64
from flask import Flask, render_template, request
app = Flask(__name__)

from  main import get_elbow_curve_cat, get_category_clusters


@app.route("/elbow-curve")
def get_elbow_curve():
    cat_name = request.args.get("cat")
    plot_url = get_elbow_curve_cat(cat_name)
    return render_template('test.html', plot_url=plot_url)


@app.route("/price-range")
def get_price_range():
    cat_name = request.args.get("cat")
    return get_category_clusters(cat_name)


if __name__ == "__main__":
    app.run(debug=True)
    print "yes"