from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

ALLOWED_MEDIA_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'avi', 'mov'}

def allowed_media_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_MEDIA_EXTENSIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///psicologia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos de Base de Datos
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(120), nullable=False)
    email_cliente = db.Column(db.String(120), nullable=False)
    telefono_cliente = db.Column(db.String(20), nullable=False)
    fecha_cita = db.Column(db.String(50), nullable=False)
    hora_cita = db.Column(db.String(10), nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.now)
    confirmada = db.Column(db.Boolean, default=False)

class Testimonio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(120), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    calificacion = db.Column(db.Integer, default=5)
    fecha = db.Column(db.DateTime, default=datetime.now)
    aprobado = db.Column(db.Boolean, default=False)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'foto' o 'video'
    descripcion = db.Column(db.Text, nullable=True)
    fecha_subida = db.Column(db.DateTime, default=datetime.now)
    visible = db.Column(db.Boolean, default=True)

class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    icono = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    orden = db.Column(db.Integer, default=0)

class Precio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    monto = db.Column(db.Integer, nullable=False)
    duracion = db.Column(db.String(50), nullable=True)
    destacado = db.Column(db.Boolean, default=False)
    orden = db.Column(db.Integer, default=0)

# Crear tablas
with app.app_context():
    db.create_all()
    # Crear admin por defecto si no existe
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(
            username='admin',
            password=generate_password_hash('123456'),
            email='admin@psicologia.com'
        )
        db.session.add(admin)
        db.session.commit()
    
    # Crear servicios por defecto si no existen
    if Servicio.query.count() == 0:
        servicios_default = [
            Servicio(nombre='Terapia Individual', icono='🧠', descripcion='Sesiones personalizadas para trabajar en tus problemas emocionales y mentales de forma confidencial y segura.', orden=1),
            Servicio(nombre='Terapia de Pareja', icono='💑', descripcion='Espacios de escucha activa para mejorar la comunicación y fortalecer tu relación de pareja.', orden=2),
            Servicio(nombre='Terapia Familiar', icono='👨‍👩‍👧‍👦', descripcion='Intervención profesional para resolver conflictos y mejorar las dinámicas familiares.', orden=3),
            Servicio(nombre='Manejo de Ansiedad', icono='😰', descripcion='Técnicas y estrategias para reducir la ansiedad y recuperar el bienestar emocional.', orden=4),
            Servicio(nombre='Depresión y Duelo', icono='😔', descripcion='Apoyo emocional para superar momentos difíciles y procesar pérdidas de forma saludable.', orden=5),
            Servicio(nombre='Apoyo Espiritual', icono='🙏', descripcion='Integración de valores cristianos en el proceso terapéutico para tu bienestar integral.', orden=6),
        ]
        db.session.add_all(servicios_default)
        db.session.commit()
    
    # Crear precios por defecto si no existen
    if Precio.query.count() == 0:
        precios_default = [
            Precio(nombre='Sesión Individual', descripcion='Primera consulta', monto=80000, duracion='60 minutos', destacado=False, orden=1),
            Precio(nombre='Sesión Individual', descripcion='Sesiones subsecuentes', monto=70000, duracion='60 minutos', destacado=True, orden=2),
            Precio(nombre='Terapia de Pareja', descripcion='Por sesión', monto=100000, duracion='90 minutos', destacado=False, orden=3),
            Precio(nombre='Terapia Familiar', descripcion='Por sesión', monto=120000, duracion='90 minutos', destacado=False, orden=4),
            Precio(nombre='Consulta por Teléfono', descripcion='Sesión virtual', monto=50000, duracion='30 minutos', destacado=False, orden=5),
            Precio(nombre='Paquete Semestral', descripcion='6 sesiones de 60 min', monto=350000, duracion='Ahorra $70.000', destacado=False, orden=6),
        ]
        db.session.add_all(precios_default)
        db.session.commit()

# Rutas
@app.route('/')
def index():
    testimonios = Testimonio.query.filter_by(aprobado=True).all()
    servicios = Servicio.query.order_by(Servicio.orden).all()
    precios = Precio.query.order_by(Precio.orden).all()
    return render_template('index.html', testimonios=testimonios, servicios=servicios, precios=precios)

@app.route('/galeria')
def galeria():
    media = Media.query.filter_by(visible=True).order_by(Media.fecha_subida.desc()).all()
    fotos = [m for m in media if m.tipo == 'foto']
    videos = [m for m in media if m.tipo == 'video']
    return render_template('galeria.html', fotos=fotos, videos=videos)

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        try:
            nueva_cita = Cita(
                nombre_cliente=request.form['nombre'],
                email_cliente=request.form['email'],
                telefono_cliente=request.form['telefono'],
                fecha_cita=request.form['fecha'],
                hora_cita=request.form['hora'],
                motivo=request.form['motivo']
            )
            db.session.add(nueva_cita)
            db.session.commit()
            flash('¡Cita agendada exitosamente! Te contactaremos pronto.', 'success')
            return redirect('/')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return render_template('agendar.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash('¡Bienvenido!', 'success')
            return redirect('/admin/dashboard')
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    citas = Cita.query.order_by(Cita.fecha_registro.desc()).all()
    testimonios = Testimonio.query.all()
    citas_por_confirmar = Cita.query.filter_by(confirmada=False).count()
    medios = Media.query.order_by(Media.fecha_subida.desc()).all()
    
    return render_template('admin_dashboard.html', 
                         citas=citas, 
                         testimonios=testimonios,
                         citas_por_confirmar=citas_por_confirmar,
                         medios=medios)

@app.route('/admin/confirmar_cita/<int:cita_id>', methods=['POST'])
def confirmar_cita(cita_id):
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    cita = Cita.query.get(cita_id)
    if cita:
        cita.confirmada = True
        db.session.commit()
        flash('Cita confirmada', 'success')
    return redirect('/admin/dashboard')

@app.route('/admin/eliminar_cita/<int:cita_id>', methods=['POST'])
def eliminar_cita(cita_id):
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    cita = Cita.query.get(cita_id)
    if cita:
        db.session.delete(cita)
        db.session.commit()
        flash('Cita eliminada', 'success')
    return redirect('/admin/dashboard')

@app.route('/admin/aprobar_testimonio/<int:testimonio_id>', methods=['POST'])
def aprobar_testimonio(testimonio_id):
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    testimonio = Testimonio.query.get(testimonio_id)
    if testimonio:
        testimonio.aprobado = True
        db.session.commit()
        flash('Testimonio aprobado', 'success')
    return redirect('/admin/dashboard')

@app.route('/admin/eliminar_media/<int:media_id>', methods=['POST'])
def eliminar_media(media_id):
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    media = Media.query.get(media_id)
    if media:
        try:
            os.remove(os.path.join('static/media', media.filename))
        except:
            pass
        db.session.delete(media)
        db.session.commit()
        flash('Archivo eliminado', 'success')
    return redirect('/admin/dashboard')

@app.route('/admin/toggle_media/<int:media_id>', methods=['POST'])
def toggle_media(media_id):
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    media = Media.query.get(media_id)
    if media:
        media.visible = not media.visible
        db.session.commit()
        estado = 'visible' if media.visible else 'oculto'
        flash(f'Archivo marcado como {estado}', 'success')
    return redirect('/admin/dashboard')

@app.route('/admin/editar_servicios', methods=['GET', 'POST'])
def editar_servicios():
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    if request.method == 'POST':
        # Actualizar servicios existentes
        servicios = Servicio.query.all()
        for i, servicio in enumerate(servicios):
            servicio.nombre = request.form.get(f'nombre_{servicio.id}', servicio.nombre)
            servicio.descripcion = request.form.get(f'descripcion_{servicio.id}', servicio.descripcion)
            servicio.icono = request.form.get(f'icono_{servicio.id}', servicio.icono)
        db.session.commit()
        flash('Servicios actualizados correctamente', 'success')
        return redirect('/admin/dashboard')
    
    servicios = Servicio.query.order_by(Servicio.orden).all()
    return render_template('admin_editar_servicios.html', servicios=servicios)

@app.route('/admin/editar_precios', methods=['GET', 'POST'])
def editar_precios():
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    if request.method == 'POST':
        # Actualizar precios existentes
        precios = Precio.query.all()
        for i, precio in enumerate(precios):
            precio.nombre = request.form.get(f'nombre_{precio.id}', precio.nombre)
            precio.descripcion = request.form.get(f'descripcion_{precio.id}', precio.descripcion)
            precio.monto = int(request.form.get(f'monto_{precio.id}', precio.monto))
            precio.duracion = request.form.get(f'duracion_{precio.id}', precio.duracion)
            precio.destacado = f'destacado_{precio.id}' in request.form
        db.session.commit()
        flash('Precios actualizados correctamente', 'success')
        return redirect('/admin/dashboard')
    
    precios = Precio.query.order_by(Precio.orden).all()
    return render_template('admin_editar_precios.html', precios=precios)

@app.route('/admin/upload_profile', methods=['POST'])
def upload_profile():
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    if 'file' not in request.files:
        flash('No se seleccionó archivo', 'danger')
        return redirect('/admin/dashboard')
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No se seleccionó archivo', 'danger')
        return redirect('/admin/dashboard')
    
    if file and allowed_file(file.filename):
        filename = secure_filename('profile.jpg')
        filepath = os.path.join('static/images', filename)
        os.makedirs('static/images', exist_ok=True)
        file.save(filepath)
        flash('Foto de perfil actualizada correctamente', 'success')
    else:
        flash('Formato de archivo no permitido (usa PNG, JPG, JPEG o GIF)', 'danger')
    
    return redirect('/admin/dashboard')

@app.route('/admin/upload_media', methods=['POST'])
def upload_media():
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    if 'file' not in request.files:
        flash('No se seleccionó archivo', 'danger')
        return redirect('/admin/dashboard')
    
    file = request.files['file']
    tipo = request.form.get('tipo', 'foto')
    descripcion = request.form.get('descripcion', '')
    
    if file.filename == '':
        flash('No se seleccionó archivo', 'danger')
        return redirect('/admin/dashboard')
    
    if file and allowed_media_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
        filepath = os.path.join('static/media', filename)
        os.makedirs('static/media', exist_ok=True)
        file.save(filepath)
        
        media = Media(
            filename=filename,
            tipo=tipo,
            descripcion=descripcion,
            visible=True
        )
        db.session.add(media)
        db.session.commit()
        flash('Archivo subido correctamente', 'success')
    else:
        flash('Formato de archivo no permitido', 'danger')
    
    return redirect('/admin/dashboard')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
