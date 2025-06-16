import random
import sys, argparse
import numpy as np

def random_labels(G, T, L):
    labels = np.arange(L)
    labels_per_guest = [random.randint(1, int(L/4)+1) for g in range(G)]
    guest_labels = []
    for g in range(G):
        guest_labels.append(np.random.choice(labels, labels_per_guest[g], replace=False))

    return guest_labels

def random_label_weight(L, maxw):
    return np.random.randint(1, maxw+1, L)

def random_disagreements(G, d):
    guests_ix = np.arange(G)
    D = np.array([np.random.choice(guests_ix, 2, replace=False) for di in range(d)])
    D = np.unique(D, axis=0)
    return list(D)


# def save_pb(fname, G, guest_labels, T, L, D):
    # pass

def save_raw(fname, G, guest_labels, T, L, W, D, l, u):
    f = open(fname, "w")
    f.write(f"# {G} guests, {T} tables, {L} labels, {len(D)} disagreements, {l} to {u} guests per table\n")
    f.write(f"{G} {T} {L} {len(D)} {l} {u}\n")
    f.write(f"# Label weight\n")
    f.write(f"{' '.join(map(str, W))}\n")
    f.write("# Labels associated to each guest\n")
    for gl in guest_labels:
        f.write(f"{' '.join(map(str, gl))}\n")
    f.write("# Disagreements\n")
    for di in D:
        f.write(f"{' '.join(map(str, di))}\n")

    f.close()

#TODO
def save_pbo(fname, G, guest_labels, T, L, W, D, l, u):
    pass


def readArguments():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
        description="Generate instances for the Seating Arrangement Problem\n"
        )

    parser.add_argument("-o", type=str, default="../../../data/instances/", help="output folder")
    parser.add_argument("-G", type=int, default=10, help="number of guests")
    parser.add_argument("-T", type=int, default=3, help="number of tables")
    parser.add_argument("-l", type=int, default=2, help="minimum number of guests per table")
    parser.add_argument("-u", type=int, default=5, help="maximum number of guests per table")
    parser.add_argument("-L", type=int, default=10, help="number of labels")
    parser.add_argument("-d", type=int, default=0, help="maximum number of disagreements")
    parser.add_argument("-W", type=int, default=10, help="maximum label weight (between 1 and 10)")
    args = parser.parse_args(sys.argv[1:])
    print ("args: %r\n" % args)

    if args.G/args.u > args.T:
        raise ValueError("There are not enough tables")
    if args.G/args.T < args.l:
        raise ValueError("There are too many tables")
    if args.l > args.u:
        raise ValueError("l cannot be greater than u")
    if args.W < 1 or args.W > 10:
        raise ValueError("W must be a number between 1 and 10")

    return args.o, args.G, args.T, args.l, args.u, args.L, args.d, args.W



if __name__ == "__main__":
    # G = 10
    # T = 3
    # l, u = 2,5
    # L = 10
    # d = 2
    # maxw = 10

    folder, G, T, l, u, L, d, maxw = readArguments()

    guest_labels = random_labels(G, T, L)
    D = random_disagreements(G, d)
    W = random_label_weight(L, maxw)
    fname = folder+f"/sap_{G}G_{T}T_{l}l_{u}u_{L}L_{len(D)}d_{maxw}w.in"
    save_raw(fname, G, guest_labels, T, L, W, D, l, u)
