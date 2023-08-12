from flask import (Blueprint, render_template,
                   request, flash, redirect, url_for, current_app)

import resend

from app.db import get_db

bp = Blueprint('mail', __name__, url_prefix='/')


@ bp.route('/', methods=['GET'])
def index():
    search = request.args.get('search')

    db, c = get_db()
    if search is None:
        c.execute('SELECT * FROM email')
    else:
        c.execute("SELECT * FROM email WHERE content like %s",
                  ('%' + search + '%',))

    mails = c.fetchall()
    return render_template('mails/index.html', mails=mails)


@ bp.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')
        errors = []

        if not email:
            errors.append('El email es obligatorio')

        if not subject:
            errors.append('El asunto del correo es obligatorio')

        if not content:
            errors.append('El contenido del correo es obligatorio')

        if len(errors) == 0:
            send(email, subject, content)
            db, c = get_db()
            c.execute("INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)",
                      (email, subject, content))
            db.commit()

            return redirect(url_for('mail.index'))
        else:
            for error in errors:
                flash(error)

        print(errors)

    return render_template('mails/create.html')


def send(to, subject, content):
    resend.api.key = current_app.config['RESEND_API_KEY']
    params = {
        "from": "MailerApp <onboarding@resend.dev>",
        "to": to,
        "subject": subject,
        "html": content

    }
    email = resend.Emails.send(params)
