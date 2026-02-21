import sqlite3
conn = sqlite3.connect('crabs.db')
c = conn.cursor()

print("=== KEY_NODES ===")
c.execute("SELECT * FROM key_nodes ORDER BY id")
for row in c.fetchall():
    print(row)

print("\n=== KEY_OPTIONS ===")
c.execute("SELECT * FROM key_options ORDER BY node_id, id")
for row in c.fetchall():
    print(row)

print("\n=== ALL SPECIES ===")
c.execute("SELECT id, name, genus, family, color, size, location, spines, appendages, carapace_lines, posterior_spines, cardiac_spines, antennular_spine, supraocular_spines, fourth_abdominal_spine, abdominal_midline_spines, rostrum_spines, ocular_peduncle_spines, gastric_spines FROM species")
cols = [d[0] for d in c.description]
print(cols)
for row in c.fetchall():
    print(row)

conn.close()
