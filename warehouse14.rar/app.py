from flask import Flask, render_template, request, redirect, url_for, flash
from database import (
    init_db, get_products, get_product, add_product, update_product,
    update_quantity, delete_product, get_categories
)

app = Flask(__name__)
app.secret_key = '1234'  # ключ

init_db() # БАЗА ДАННЫХ

LOW_STOCK_THRESHOLD = 5

@app.route('/') # декоратор главная страница
def index():
    sort_by = request.args.get('sort', 'id_desc') 
    category = request.args.get('category', 'all')
    
    products = get_products(sort_by=sort_by, category_filter=category)
    categories = get_categories()
    
    return render_template('index.html', 
                         products=products, 
                         categories=categories,
                         selected_category=category,
                         selected_sort=sort_by,
                         low_stock_threshold=LOW_STOCK_THRESHOLD)

@app.route('/product/add', methods=['GET', 'POST']) # декоратор добавления товара
def add_product_route():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        quantity = request.form.get('quantity', '')
        price = request.form.get('price', '')
        supplier = request.form.get('supplier', '').strip()
        
        errors = []
        if not name:
            errors.append('Название товара обязательно')
        if not category:
            errors.append('Категория обязательна')
        if not quantity or not quantity.replace('-', '').isdigit():
            errors.append('Количество должно быть целым числом')
        elif int(quantity) < 0:
            errors.append('Количество не может быть отрицательным')
        if not price:
            errors.append('Цена обязательна')
        else:
            try:
                price_val = float(price)
                if price_val < 0:
                    errors.append('Цена не может быть отрицательной')
            except ValueError:
                errors.append('Цена должна быть числом')
        if not supplier:
            errors.append('Поставщик обязателен')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('product_form.html', product=None, categories=get_categories())
        
        add_product(name, category, int(quantity), float(price), supplier)
        flash('Товар успешно добавлен', 'success')
        return redirect(url_for('index'))
    
    return render_template('product_form.html', product=None, categories=get_categories())

@app.route('/product/<int:product_id>/edit', methods=['GET', 'POST']) # декоратор изменения товара
def edit_product_route(product_id):
    product = get_product(product_id)
    if not product:
        flash('Товар не найден', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        quantity = request.form.get('quantity', '')
        price = request.form.get('price', '')
        supplier = request.form.get('supplier', '').strip()
        
        errors = []
        if not name:
            errors.append('Название товара обязательно')
        if not category:
            errors.append('Категория обязательна')
        if not quantity or not quantity.replace('-', '').isdigit():
            errors.append('Количество должно быть целым числом')
        elif int(quantity) < 0:
            errors.append('Количество не может быть отрицательным')
        if not price:
            errors.append('Цена обязательна')
        else:
            try:
                price_val = float(price)
                if price_val < 0:
                    errors.append('Цена не может быть отрицательной')
            except ValueError:
                errors.append('Цена должна быть числом')
        if not supplier:
            errors.append('Поставщик обязателен')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('product_form.html', product=product, categories=get_categories())
        
        update_product(product_id, name, category, int(quantity), float(price), supplier)
        flash('Товар успешно обновлён', 'success')
        return redirect(url_for('index'))
    
    return render_template('product_form.html', product=product, categories=get_categories())

@app.route('/product/<int:product_id>/update_quantity', methods=['POST']) # декоратор изменения количества товара
def update_quantity_route(product_id):
    product = get_product(product_id)
    if not product:
        flash('Товар не найден', 'error')
        return redirect(url_for('index'))
    
    action = request.form.get('action')
    current_quantity = product['quantity']
    
    if action == 'increase':
        new_quantity = current_quantity + 1
    elif action == 'decrease':
        new_quantity = max(0, current_quantity - 1)
    else:
        return redirect(url_for('index'))
    
    update_quantity(product_id, new_quantity)
    flash(f'Количество товара "{product["name"]}" изменено с {current_quantity} на {new_quantity}', 'success')
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>/delete', methods=['POST']) # декоратор удаления
def delete_product_route(product_id):
    product = get_product(product_id)
    if product:
        delete_product(product_id)
        flash(f'Товар "{product["name"]}" удалён', 'success')
    else:
        flash('Товар не найден', 'error')
    return redirect(url_for('index'))

@app.route('/low_stock') # декоратор малые остатки
def low_stock():
    sort_by = request.args.get('sort', 'id_desc')
    products = get_products(sort_by=sort_by, low_stock_threshold=LOW_STOCK_THRESHOLD)
    categories = get_categories()
    
    return render_template('low_stock.html',
                         products=products,
                         categories=categories,
                         threshold=LOW_STOCK_THRESHOLD,
                         selected_sort=sort_by)

if __name__ == '__main__':
    app.run(debug=True)

# Запуск - python3 app.py run 