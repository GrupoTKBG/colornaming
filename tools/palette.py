import sys
import argparse
from joblib import Memory, Parallel, delayed
from colornaming import list_known_models, get_model
from colornaming.img import QImage
from colornaming.palette import Palette

parser = argparse.ArgumentParser(
                    prog='qpalette',
                    description='Get image palette information using qualitative colors')

parser.add_argument('images', nargs='+', help='images to analyze')
parser.add_argument("-m", "--model", choices=list_known_models(), default="qcd", help="model to use")    
parser.add_argument("--method", choices=["colorthief", "qualitative"], default="colorthief", help="method to use for palette extraction")
parser.add_argument("--moods", type=int, default=0, help="get N kobayashi moods")    
parser.add_argument("-n", "--num-colors", type=int, default=5, help="Number of colors in palette")
parser.add_argument("-s", "--max_size", nargs=2, required=False, default=[244, 244], help="Scale the image to this maximum size")
parser.add_argument("-j", "--jobs", required=False, type=int, default=1, help="Number of joblib parallel jobs")
parser.add_argument("-c", "--cache", required=False, default=None, help="Use this directory as joblib cache")
parser.add_argument("-o", "--outfile", required=False, default=None, help="Output file")
parser.add_argument("--header", required=False, default=False, action='store_true', help="Output CSV header")
parser.add_argument("--score", required=False, default=False, action='store_true', help="Score the palette")

args = parser.parse_args()
args.max_size = tuple(args.max_size)


def get_top_colors(qimg, fname, model, num_colors):
    return qimg.top_colors(num_colors)

def get_moods(qimg, fname, model, num_moods):
    return qimg.top_moods(num_moods)

def get_score(top_colors, model):
    pal = Palette([c[0] for c in top_colors], model)
    return pal.score_palette()

def process_image(f, args, model):
    qimg = QImage(f, model=model, max_size=args.max_size)
    top_colors= get_top_colors(qimg, f, args.model, args.num_colors)
    res = f'"{f}"' + "," + f"{','.join([f'{c[0]},{c[1]}' for c in top_colors])}"
    
    if args.moods > 0:
        moods = get_moods(qimg, f, args.model, args.moods)
        res += ',' + ','.join([f"{m[0]},{m[1]}" for m in moods])
        for i in range(len(moods), args.moods):
            res += ",,"
    if args.score:
        res += ',' + f"{get_score(top_colors, model):.3f}"
    return res

def process_colorthief(f, args, model):
    from colorthief import ColorThief
    ct = ColorThief(f)
    palette = ct.get_palette(color_count=args.num_colors)
    qpalette = [model.from_rgb(*[c/255.0 for c in p]) for p in palette]
    # res = f'"{f}"' + "," + f"{','.join([f'{c},{1/len(palette):.3f}' for c in palette])}"
    res = ",".join(qpalette)
    return res

if args.cache:
    mem = Memory(args.cache, verbose=0)
    get_top_colors = mem.cache(get_top_colors, ignore=['qimg']) # type: ignore
    get_moods = mem.cache(get_moods, ignore=['qimg']) # type: ignore
    get_score = mem.cache(get_score) # type: ignore

model = get_model(args.model)
if args.header:
    header = 'image' + "," + ",".join([f"color{i+1},color_weight{i+1}" for i in range(args.num_colors)])
    if args.moods > 0:
        header += "," + ",".join([f"mood{i+1},mood_weight{i+1}" for i in range(args.moods)])
    if args.score:
        header += ",score"
    print(header)
outfile = sys.stdout if args.outfile is None else open(args.outfile, "wt", encoding='utf-8')
with outfile:
    if args.jobs == 1:
        for f in args.images:
            if args.method == "colorthief":
                print(process_colorthief(f, args, model), file=outfile)
            else:   
                print(process_image(f, args, model), file=outfile)
    else:
        for res in Parallel(n_jobs=args.jobs, return_as="generator", batch_size=1, verbose=10)(delayed(process_image)(f, args, model) for f in args.images): # type: ignore
            print(res, file=outfile)

