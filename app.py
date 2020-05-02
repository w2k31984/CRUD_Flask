#comenzamos nuestra aplicacion llamando nuestro framework
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#llamando a sqlAlchemy y la conexion con sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#Inicializando nuestra base de datos
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    data_create = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
       task_content = request.form['content']
       new_task = Todo(content=task_content)

       try:
           db.session.add(new_task)
           db.session.commit()
           return redirect('/')

       except:
           return 'Su Tarea ha sido agregada con Exito!'    
    else:  
        tasks = Todo.query.order_by(Todo.data_create).all()  
        return render_template('index.html', tasks=tasks)

#creando la funcion eliminar para nuestro enlace
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
           return 'Hubo un problema al eliminar esta tarea'

#creando la funcion actualizar para nuestro enlace
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Hubo un problema al actualizar su tarea'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
# La app en modo debug nos ayuda a poder ir probando la aplicacion. debug=True
    app.run(debug=True)