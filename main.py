# ============================
# Projet Floyd–Warshall (ULTRA SIMPLE)
# - Lit un ou plusieurs graphes depuis /data/*.txt
# - Affiche W (arcs), puis L et P à l'initialisation et après chaque k
# - Détecte un cycle négatif (circuit absorbant)
# - Affichage "propre" : cellules de largeur fixe, X pour l'infini
# ============================

import os


# ============================
# 1) Découverte des fichiers de graphes
# ============================

base = os.path.join(os.path.dirname(__file__), "data")

files = []
for name in os.listdir(base):
    if name.endswith(".txt"):
        files.append(name)
files.sort()

# Affiche la liste numérotée
i = 0
while i < len(files):
    print(str(i + 1) + ". " + files[i])
    i += 1

print("Tape des numéros séparés par des espaces (ex: 1 3) ou 'all'")
sel = input("> ").strip().lower()


# ============================
# 2) Sélection des fichiers à traiter
#    - 'all' = tous les fichiers
#    - sinon : liste de numéros valides
# ============================

if sel == "all":
    idxs = []
    k = 1
    while k <= len(files):
        idxs.append(k)
        k += 1
else:
    parts = sel.split()
    idxs = []
    p = 0
    while p < len(parts):
        token = parts[p]
        ok = True
        q = 0
        while q < len(token):
            ch = token[q]
            if ch < '0' or ch > '9':
                ok = False
                break
            q += 1
        if ok:
            k = int(token)
            if 1 <= k <= len(files):
                idxs.append(k)
        p += 1


# ============================
# 3) Petites fonctions d'affichage/formatage
#    - print_box_matrix : imprime une matrice de chaînes avec titre + étape
#    - to_str_from_D    : convertit D (numérique) en chaînes ("X" pour INF)
#    - to_str_from_Next : convertit Next (entier/-1) en chaînes ("X" si -1)
# ============================

def print_box_matrix(A, title, step, n, ri_w):
    # Calcule la largeur minimale de cellule
    cell_w = 1
    j = 0
    while j < n:
        if len(str(j)) > cell_w:
            cell_w = len(str(j))
        j += 1

    # Ajuste selon le contenu de la matrice
    i2 = 0
    while i2 < n:
        j2 = 0
        while j2 < n:
            if len(A[i2][j2]) > cell_w:
                cell_w = len(A[i2][j2])
            j2 += 1
        i2 += 1

    # Titre + en-tête des colonnes
    print("Étape " + str(step) + " — " + title)
    header = " " * (ri_w + 1)
    j = 0
    while j < n:
        s = str(j)
        header = header + " " + s.rjust(cell_w) + " "
        if j < n - 1:
            header = header + " "
        j += 1
    print(header)

    # Lignes de la matrice
    i2 = 0
    while i2 < n:
        row_str = str(i2).rjust(ri_w) + " "
        j2 = 0
        while j2 < n:
            row_str = row_str + " " + A[i2][j2].rjust(cell_w) + " "
            if j2 < n - 1:
                row_str = row_str + " "
            j2 += 1
        print(row_str)
        i2 += 1
    print()


def to_str_from_D(D, INF, n):
    T = []
    i3 = 0
    while i3 < n:
        row = []
        j3 = 0
        while j3 < n:
            if D[i3][j3] == INF:
                row.append("X")
            else:
                row.append(str(D[i3][j3]))
            j3 += 1
        T.append(row)
        i3 += 1
    return T


def to_str_from_Next(Next, n):
    T = []
    i3 = 0
    while i3 < n:
        row = []
        j3 = 0
        while j3 < n:
            if Next[i3][j3] == -1:
                row.append("X")
            else:
                row.append(str(Next[i3][j3]))
            j3 += 1
        T.append(row)
        i3 += 1
    return T


# ============================
# 4) Traitement de chaque graphe sélectionné
#    - Lecture du fichier (n, m, arcs)
#    - Construction de W sous forme de chaînes (S)
#    - Conversion en D (numérique) + initialisation de Next
#    - Floyd–Warshall (triple boucle) avec affichages L/P à chaque étape
#    - Détection de cycle négatif
# ============================

r = 0
while r < len(idxs):
    idx = idxs[r]
    path = os.path.join(base, files[idx - 1])

    # ---- Lecture du graphe ----
    f = open(path, "r", encoding="utf-8")
    n = int(f.readline().strip())
    m = int(f.readline().strip())

    # S : matrice des arcs (chaînes) — 0 sur diag, "X" sinon
    S = []
    i = 0
    while i < n:
        row = []
        j = 0
        while j < n:
            if i == j:
                row.append("0")
            else:
                row.append("X")
            j += 1
        S.append(row)
        i += 1

    # Remplissage des arcs depuis le fichier
    t = 0
    while t < m:
        line = f.readline()
        if not line:
            break
        u_str, v_str, w_str = line.split()
        u = int(u_str); v = int(v_str); w = int(w_str)
        S[u][v] = str(w)
        t += 1

    f.close()

    # ---- Affichages initiaux ----
    ri_w = len(str(n - 1))
    step = 1

    print("=== " + files[idx - 1] + " ===")
    print_box_matrix(S, "W (arcs)", step, n, ri_w)
    step += 1

    # D : matrice des distances (numérique) — "X" -> INF
    INF = 10**12
    D = []
    i = 0
    while i < n:
        row = []
        j = 0
        while j < n:
            if S[i][j] == "X":
                row.append(INF)
            else:
                row.append(int(S[i][j]))
            j += 1
        D.append(row)
        i += 1

    # Next : successeur immédiat pour reconstruire un chemin
    Next = []
    i = 0
    while i < n:
        row = []
        j = 0
        while j < n:
            if i == j:
                row.append(i)
            else:
                if D[i][j] != INF:
                    row.append(j)
                else:
                    row.append(-1)
            j += 1
        Next.append(row)
        i += 1

    print_box_matrix(to_str_from_D(D, INF, n), "L (distances) — initial (D^0)", step, n, ri_w)
    step += 1

    print_box_matrix(to_str_from_Next(Next, n), "P (successeurs) — initial (P^0)", step, n, ri_w)
    step += 1

    # ---- Algorithme de Floyd–Warshall ----
    # Améliore D[i][j] via un sommet intermédiaire k
    k = 0
    while k < n:
        i = 0
        while i < n:
            j = 0
            while j < n:
                if D[i][k] != INF and D[k][j] != INF:
                    newv = D[i][k] + D[k][j]
                    if newv < D[i][j]:
                        D[i][j] = newv
                        Next[i][j] = Next[i][k]
                j += 1
            i += 1

        # Affiche L et P après l'étape k
        print_box_matrix(to_str_from_D(D, INF, n), "L (distances) — k = " + str(k), step, n, ri_w)
        step += 1

        print_box_matrix(to_str_from_Next(Next, n), "P (successeurs) — k = " + str(k), step, n, ri_w)
        step += 1

        k += 1

    # ---- Détection d'un cycle négatif (circuit absorbant) ----
    neg = False
    i = 0
    while i < n:
        if D[i][i] < 0:
            neg = True
            break
        i += 1

    if neg:
        print("Circuit absorbant détecté")
    else:
        print("Pas de circuit absorbant")

    print()
    r += 1
