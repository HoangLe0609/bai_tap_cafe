import math
from flask import Flask, render_template, request, abort

app = Flask(__name__)

SHOP = {"name": "Cà phê Sông Hương",
        "address": "12 Lê Lợi, Huế",
        "phone": "0234 3888 999"}
PROMOTION = ["Giảm 10% cho sinh viên",
             "Mua 2 tặng 1 vào thứ Hai"]
MENU = [
    {"id": 1, "name": "Cà phê đen", "price": 20000, "image": "ca-phe-den.jpg"},
    {"id": 2, "name": "Cà phê sữa", "price": 25000, "image": "ca-phe-sua.jpg"},
    {"id": 3, "name": "Bạc xỉu", "price": 30000, "image": "bac-xiu.jpg"},
    {"id": 4, "name": "Trà đào", "price": 35000, "image": "tra-dao.jpg"},
    {"id": 5, "name": "Trà sữa", "price": 35000, "image": "tra-sua.jpg"},
    {"id": 6, "name": "Nước cam", "price": 30000, "image": "nuoc-cam.jpg"},
    {"id": 7, "name": "Sinh tố bơ", "price": 40000, "image": "sinh-to-bo.jpg"},
]

@app.route("/")
def index():
    return render_template('index.html', shop=SHOP)

@app.template_filter("vnd")
def vnd_format(price):
    if price is None:
        return "0 VND"
    formatted_price = f"{int(price):,}".replace(",", ".")
    return f"{formatted_price} VND"
    
@app.route("/menu")
def menu():
    page_param = request.args.get('page', '1')
        
    # Nếu page_param không phải là số hợp lệ -> Xử lý như trang 1
    try:
        page = int(page_param)
    except ValueError:
        page = 1

    per_page = 3
    total_items = len(MENU)
    pages = math.ceil(total_items / per_page) if total_items > 0 else 1

    # Nếu page = 0 hoặc page > tổng số trang -> Trả về lỗi 404
    if page < 1 or page > pages:
        abort(404)

    # Cắt danh sách món tương ứng với trang hiện tại
    start = (page - 1) * per_page
    end = start + per_page
    current_items = MENU[start:end]

    return render_template('menu.html', shop=SHOP, menu=current_items, page=page, pages=pages)

@app.route("/contact")
def contact():
    return render_template('contact.html', shop=SHOP)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', shop=SHOP), 404

if __name__ == "__main__":
    app.run(debug=True)