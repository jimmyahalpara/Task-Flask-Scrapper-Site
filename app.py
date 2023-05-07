from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # sku column as index (not unique) 
    sku = db.Column(db.String(80), index=True, nullable=False)

    price_1 = db.Column(db.Float, nullable=True)
    has_sale_1 = db.Column(db.Boolean, nullable=True)
    contractor_1 = db.Column(db.String(80), nullable=True)
    
    price_2 = db.Column(db.Float, nullable=True)
    has_sale_2 = db.Column(db.Boolean, nullable=True)
    contractor_2 = db.Column(db.String(80), nullable=True)

    price_3 = db.Column(db.Float, nullable=True)
    has_sale_3 = db.Column(db.Boolean, nullable=True)
    contractor_3 = db.Column(db.String(80), nullable=True)

    price_4 = db.Column(db.Float, nullable=True)
    has_sale_4 = db.Column(db.Boolean, nullable=True)
    contractor_4 = db.Column(db.String(80), nullable=True)

    price_5 = db.Column(db.Float, nullable=True)
    has_sale_5 = db.Column(db.Boolean, nullable=True)
    contractor_5 = db.Column(db.String(80), nullable=True)

    price_6 = db.Column(db.Float, nullable=True)
    has_sale_6 = db.Column(db.Boolean, nullable=True)
    contractor_6 = db.Column(db.String(80), nullable=True)

    price_7 = db.Column(db.Float, nullable=True)
    has_sale_7 = db.Column(db.Boolean, nullable=True)
    contractor_7 = db.Column(db.String(80), nullable=True)

    price_8 = db.Column(db.Float, nullable=True)
    has_sale_8 = db.Column(db.Boolean, nullable=True)
    contractor_8 = db.Column(db.String(80), nullable=True)

    price_9 = db.Column(db.Float, nullable=True)
    has_sale_9 = db.Column(db.Boolean, nullable=True)
    contractor_9 = db.Column(db.String(80), nullable=True)

    price_10 = db.Column(db.Float, nullable=True)
    has_sale_10 = db.Column(db.Boolean, nullable=True)
    contractor_10 = db.Column(db.String(80), nullable=True)


    def __repr__(self):
        return '<Product %r>' % self.sku
    

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)