"""
Database initialization script
Run this to reset the database with demo data
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.database import clear_all_data, init_db, create_rendicion, create_notificacion
from data.demo import get_demo_data, get_demo_notifications

def reset_database():
    """Reset database with demo data"""
    print("Clearing existing data...")
    clear_all_data()
    
    print("Initializing database...")
    init_db()
    
    print("Loading demo rendiciones...")
    rends = get_demo_data()
    for rid, rend in rends.items():
        create_rendicion(rend)
    print(f"  → {len(rends)} rendiciones loaded")
    
    print("Loading demo notifications...")
    notifs = get_demo_notifications()
    for notif in notifs:
        create_notificacion(notif)
    print(f"  → {len(notifs)} notifications loaded")
    
    print("Database reset completed successfully!")

if __name__ == "__main__":
    reset_database()
