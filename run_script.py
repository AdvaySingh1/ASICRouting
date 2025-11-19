import subprocess
import os

""" 
python3 route.py -g=simple.grid -n=simple.nl -o=simple.route
"""

if __name__=="__main__":
    grid_files = sorted([f for f in os.listdir('..') if f.endswith('.grid')], key=lambda x: x[:x.find('.')])
    netlist_files = sorted([f for f in os.listdir('..') if f.endswith('.nl')], key=lambda x: x[:x.find('.')])

    for g_f, n_f in zip(grid_files, netlist_files):
        o_f = g_f[:g_f.find('.')] + '.route'
        g_f, n_f, o_f = '../' + g_f, '../' + n_f, '../' + o_f
        print(f"python3 route.py -g={g_f} -n={n_f} -o={o_f}")

        # if (g_f == '../bench1.grid'):
        subprocess.run(['python3', '-O', 'route.py', f'-g={g_f}', f'-n={n_f}', f'-o={o_f}'])
        # subprocess.run(['pwd'], cwd="ASICRouting")


    # print(os.environ)