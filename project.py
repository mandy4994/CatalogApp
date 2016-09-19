from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine,asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
app = Flask(__name__)


engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# JSON APIs to view Category Information
@app.route('/category/<int:category_id>/menu/JSON')
def CategoryMenuJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/category/<int:category_id>/menu/<int:item_id>/JSON')
def menuItemJSON(category_id, item_id):
    Item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=Item.serialize)


@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

# Show all categories
@app.route('/')
@app.route('/categories')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('categories.html', categories = categories)


# Crete a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        flash('New Category %s Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')

# Edit a category


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category=editedCategory)


# Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)


# Show Category Items   
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/menu')
def showMenu(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template('menu.html', category=category, items=items)

# Route for new category item function


@app.route('/category/<int:category_id>/new', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if request.method == 'POST':
        print "In post method"
        newItem = Item(name=request.form['name'], description=request.form['description'],
                       price=request.form['price'], category_id=category_id)
        session.add(newItem)
        session.commit()
        flash("New Item Created!")
        return redirect(url_for('showMenu', category_id=category_id))
    else:
        return render_template('newmenuitem.html', category_id=category_id)


# Route for edit category item function


@app.route('/category/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        print "Inside Post"
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash('Item Successfully edited')
        return redirect(url_for('showMenu', category_id=category_id))
    else:
        print "inside else"
        return render_template('editmenuitem.html', category_id=category_id, item_id=item_id, item=editedItem)


# Route for deleting category item function


@app.route('/category/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showMenu', category_id=category_id))
    else:
        return render_template('deletemenuitem.html', item=itemToDelete)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
