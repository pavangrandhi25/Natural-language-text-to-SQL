import sqlite3

def init_database():
    conn = sqlite3.connect('network_devices_inventory.db')
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON")

    c.execute("""CREATE TABLE IF NOT EXISTS device (
        device_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        ip_addr TEXT,
        mac_addr TEXT,
        vendor TEXT,
        location TEXT
    );""")

    c.execute("""CREATE TABLE IF NOT EXISTS interface (
        interface_id INTEGER PRIMARY KEY,
        device_id INTEGER NOT NULL,
        interface_name TEXT NOT NULL,
        interface_type TEXT NOT NULL,
        FOREIGN KEY (device_id) REFERENCES device(device_id)
    );""")

    c.execute("""CREATE TABLE IF NOT EXISTS connectivity (
        link_id INTEGER PRIMARY KEY,
        from_interface_id INTEGER NOT NULL,
        to_interface_id INTEGER NOT NULL,
        link_type TEXT NOT NULL,
        FOREIGN KEY (from_interface_id) REFERENCES interface(interface_id),
        FOREIGN KEY (to_interface_id) REFERENCES interface(interface_id)
    );""")

    c.execute("""CREATE TABLE IF NOT EXISTS mac_table (
        mac_id INTEGER PRIMARY KEY,
        switch_device_id INTEGER NOT NULL,
        mac_address TEXT NOT NULL,
        interface_id INTEGER NOT NULL,
        FOREIGN KEY (switch_device_id) REFERENCES device(device_id),
        FOREIGN KEY (interface_id) REFERENCES interface(interface_id)
    );""")

    devices = [
        (1,'R1','ROUTER','192.168.10.1','AA:AA:AA:AA:AA:01','Cisco','ServerRoom'),
        (2,'SW1','SWITCH','192.168.10.2','BB:BB:BB:BB:BB:02','Cisco','ServerRoom'),
        (3,'AP1','AP','192.168.10.3','CC:CC:CC:CC:CC:03','Cisco','Lab'),
        (4,'Laptop1','CLIENT','192.168.20.101','DD:DD:DD:DD:DD:04','Dell','Lab'),
        (5,'Phone1','CLIENT','192.168.20.102','EE:EE:EE:EE:EE:05','Apple','Lab'),
    ]
    c.executemany("INSERT OR IGNORE INTO device VALUES (?,?,?,?,?,?,?)", devices)

    interfaces = [
        (1,1,'Gi0/0','ETH'),
        (2,2,'Gi1/0/1','ETH'),
        (3,2,'Gi1/0/2','ETH'),
        (4,2,'Gi1/0/3','ETH'),
        (5,3,'eth0','ETH'),
        (6,3,'wlan0','WLAN'),
        (7,4,'wlan0','WLAN'),
        (8,5,'wlan0','WLAN'),
    ]
    c.executemany("INSERT OR IGNORE INTO interface VALUES (?,?,?,?)", interfaces)

    connectivity = [
        (1,1,2,'WIRED'),
        (2,3,5,'WIRED'),
        (3,6,7,'WIRELESS'),
        (4,6,8,'WIRELESS'),
    ]
    c.executemany("INSERT OR IGNORE INTO connectivity VALUES (?,?,?,?)", connectivity)

    mac_table = [
        (1,2,'DD:DD:DD:DD:DD:04',3),
        (2,2,'EE:EE:EE:EE:EE:05',3),
    ]
    c.executemany("INSERT OR IGNORE INTO mac_table VALUES (?,?,?,?)", mac_table)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()