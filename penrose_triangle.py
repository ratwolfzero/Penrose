import matplotlib.pyplot as plt
import numpy as np
from numba import njit
from matplotlib.patches import Polygon
import colorsys

# Golden ratio
phi = (1 + np.sqrt(5)) / 2


def subdivide_triangle(tile):
    A, B, C, tile_type = tile
    new_tiles = []
    if tile_type == 'acute':
        P = A + (B - A) / phi
        new_tiles.append((C, P, B, 'acute'))
        new_tiles.append((P, C, A, 'obtuse'))
    elif tile_type == 'obtuse':
        Q = B + (A - B) / phi
        R = B + (C - B) / phi
        new_tiles.append((R, C, A, 'obtuse'))
        new_tiles.append((Q, R, B, 'obtuse'))
        new_tiles.append((R, Q, A, 'acute'))
    return new_tiles


def iterative_subdivide(initial_tiles, depth):
    stack = [(tile, 0) for tile in initial_tiles]
    result = []

    while stack:
        tile, current_depth = stack.pop()
        if current_depth == depth:
            result.append(tile)
        else:
            subdivided = subdivide_triangle(tile)
            for t in subdivided:
                stack.append((t, current_depth + 1))

    return result


def create_initial_triangle_star():
    tiles = []
    radius = 1.0
    for i in range(10):
        angle1 = 2 * np.pi * i / 10
        angle2 = 2 * np.pi * (i + 1) / 10
        A = np.array([0, 0])
        B = radius * np.array([np.cos(angle1), np.sin(angle1)])
        C = radius * np.array([np.cos(angle2), np.sin(angle2)])
        tiles.append((A, B, C, 'acute'))
    return tiles


@njit
def get_tile_orientation_index_numba(A, C):
    vec = C - A
    angle = np.arctan2(vec[1], vec[0])
    angle = (angle + 2 * np.pi) % (2 * np.pi)
    orientation_index = int(np.round(angle / (2 * np.pi / 10))) % 10
    return orientation_index


def get_tile_orientation_index(tile):
    A, _, C, _ = tile
    return get_tile_orientation_index_numba(A, C)


def plot_triangle_tiling(tiles, output_filename=None, color_mode='color'):
    fig, ax = plt.subplots(figsize=(10, 10))
    acute_color = (1, 0.6, 0.2)
    obtuse_color = (0.2, 0.6, 1)
    orientation_colors = [colorsys.hsv_to_rgb(
        i / 10.0, 0.9, 0.9) for i in range(10)]
    gray = (0.8, 0.8, 0.8)

    for tile in tiles:
        A, B, C, tile_type = tile
        polygon = Polygon([A, B, C], closed=True)
        if color_mode == 'mono':
            colors = gray
        elif color_mode == 'type':
            colors = acute_color if tile_type == 'acute' else obtuse_color
        else:
            idx = get_tile_orientation_index(tile)
            colors = orientation_colors[idx]
        ax.add_patch(polygon)
        polygon.set_facecolor(colors)
        polygon.set_edgecolor('black')
        polygon.set_linewidth(0.3)

    ax.set_aspect('equal')
    ax.set_axis_off()

    all_points = np.array([vertex for tile in tiles for vertex in tile[:3]])
    if all_points.size > 0:
        min_x, max_x = all_points[:, 0].min(), all_points[:, 0].max()
        min_y, max_y = all_points[:, 1].min(), all_points[:, 1].max()
        padding = max((max_x - min_x) * 0.05, (max_y - min_y) * 0.05)
        ax.set_xlim(min_x - padding, max_x + padding)
        ax.set_ylim(min_y - padding, max_y + padding)

    plt.tight_layout()

    if output_filename:
        plt.savefig(output_filename, dpi=300)
    else:
        plt.show()


if __name__ == '__main__':
    print("Triangle-based Penrose-like Tiling Generator")
    print("This uses Robinson triangle subdivision rules.")

    while True:
        try:
            depth = int(input("Enter recursion depth (3–6 recommended): "))
            if depth >= 0:
                break
            print("Depth must be non-negative.")
        except ValueError:
            print("Please enter an integer.")

    while True:
        color_mode = input(
            "Color mode? 'mono' (grayscale), 'type' (acute/obtuse), or 'color' (orientation-based): ").strip().lower()
        if color_mode in ['mono', 'type', 'color']:
            break
        print("Invalid input. Please type 'mono', 'type', or 'color'.")

    output_file = input(
        "Optional: enter output filename (.png or .svg), or leave blank: ").strip()
    if output_file and not output_file.lower().endswith(('.png', '.svg')):
        print("No valid extension found; appending '.png' by default.")
        output_file += '.png'

    tiles = create_initial_triangle_star()
    tiles = iterative_subdivide(tiles, depth)
    plot_triangle_tiling(tiles, output_file if output_file else None,
                         color_mode=color_mode)
