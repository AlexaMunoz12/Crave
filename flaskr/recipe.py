from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('recipe', __name__)

@bp.route('/')
def index():
    db = get_db()
    recipes = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM recipe p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('recipe/index.html', recipes=recipes)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO recipe (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('recipe.index'))

    return render_template('recipe/create.html')

def get_recipe(id, check_author=True):
    recipe = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM recipe p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if recipe is None:
        abort(404, f"Recipe id {id} doesn't exist.")

    if check_author and recipe['author_id'] != g.user['id']:
        abort(403)

    return recipe

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    recipe = get_recipe(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE recipe SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('recipe.index'))

    return render_template('recipe/update.html', recipe=recipe)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_recipe(id)
    db = get_db()
    db.execute('DELETE FROM recipe WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('recipe.index'))