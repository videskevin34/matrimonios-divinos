from psicologia_app import app, db, Admin
from werkzeug.security import generate_password_hash

with app.app_context():
    # Buscar admin existente (por username o por cualquier admin)
    admin = Admin.query.filter_by(username='admin').first()
    
    if not admin:
        admin = Admin.query.first()
    
    if admin:
        # Actualizar usuario y contraseña
        admin.username = 'Erica'
        admin.password = generate_password_hash('matrimoniosdivinos')
        db.session.commit()
        print("✅ Admin actualizado:")
        print(f"   Usuario: {admin.username}")
        print(f"   Contraseña: matrimoniosdivinos")
    else:
        print("❌ No hay admin en la BD")

