"""
HBnB V2 — Application Entry Point
"""
import os
from app import create_app

config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    print(f"""
╔══════════════════════════════════════════╗
║         🏠 HBnB V2 — Gatherin           ║
║   منصة حجز العقارات                      ║
╠══════════════════════════════════════════╣
║  🌐 http://{host}:{port}                ║
║  📖 API: http://{host}:{port}/api/v1    ║
║  🌍 Language: AR/EN                      ║
╚══════════════════════════════════════════╝
    """)
    app.run(host=host, port=port, debug=app.config.get('DEBUG', True))
