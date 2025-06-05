import matplotlib.pyplot as plt
import numpy as np
from numba import njit
from matplotlib.collections import PolyCollection
import colorsys
from dataclasses import dataclass

# Golden ratio
phi = (1 + np.sqrt(5)) / 2


@dataclass
class Triangle:
    """Memory-efficient triangle container using float32"""
    A: np.ndarray  # Vertex A [x,y]
    B: np.ndarray  # Vertex B [x,y]
    C: np.ndarray  # Vertex C [x,y]
    tile_type: str  # 'acute' or 'obtuse'

    def __post_init__(self):
        # Ensure all vertices are float32
        self.A = self.A.astype(np.float32)
        self.B = self.B.astype(np.float32)
        self.C = self.C.astype(np.float32)


def create_initial_triangle_star():
    """Create the 10 initial acute triangles forming a star"""
    tiles = []
    radius = 1.0
    for i in range(10):
        angle1 = 2 * np.pi * i / 10
        angle2 = 2 * np.pi * (i + 1) / 10
        A = np.array([0.0, 0.0], dtype=np.float32)
        B = radius * \
            np.array([np.cos(angle1), np.sin(angle1)], dtype=np.float32)
        C = radius * \
            np.array([np.cos(angle2), np.sin(angle2)], dtype=np.float32)
        tiles.append(Triangle(A, B, C, 'acute'))
    return tiles


def subdivide_triangle(tile):
    """Robinson triangle subdivision rules"""
    new_tiles = []
    if tile.tile_type == 'acute':
        P = tile.A + (tile.B - tile.A) / phi
        new_tiles.append(Triangle(tile.C, P, tile.B, 'acute'))
        new_tiles.append(Triangle(P, tile.C, tile.A, 'obtuse'))
    else:
        Q = tile.B + (tile.A - tile.B) / phi
        R = tile.B + (tile.C - tile.B) / phi
        new_tiles.append(Triangle(R, tile.C, tile.A, 'obtuse'))
        new_tiles.append(Triangle(Q, R, tile.B, 'obtuse'))
        new_tiles.append(Triangle(R, Q, tile.A, 'acute'))
    return new_tiles


def iterative_subdivide(initial_tiles, depth):
    """Non-recursive subdivision with depth control"""
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


@njit(cache=True)
def get_orientation_index_numba(A, C):
    """Numba-optimized orientation calculation"""
    vec = C - A
    angle = np.arctan2(vec[1], vec[0])
    angle = (angle + 2 * np.pi) % (2 * np.pi)
    return int(np.round(angle / (2 * np.pi / 10))) % 10


def get_tile_orientation_index(tile):
    """Get orientation index for coloring"""
    return get_orientation_index_numba(tile.A, tile.C)


def plot_triangle_tiling(tiles, output_filename=None, color_mode='color'):
    """Optimized plotting using PolyCollection"""
    fig, ax = plt.subplots(figsize=(10, 10))

    # Color definitions
    acute_color = np.array([1, 0.6, 0.2], dtype=np.float32)
    obtuse_color = np.array([0.2, 0.6, 1], dtype=np.float32)
    gray = np.array([0.8, 0.8, 0.8], dtype=np.float32)

    # Pre-allocate arrays
    num_triangles = len(tiles)
    vertices = np.empty((num_triangles, 3, 2), dtype=np.float32)
    face_colors = np.empty((num_triangles, 3), dtype=np.float32)

    # Prepare data
    for i, tile in enumerate(tiles):
        vertices[i] = [tile.A, tile.B, tile.C]

        if color_mode == 'mono':
            face_colors[i] = gray
        elif color_mode == 'type':
            face_colors[i] = acute_color if tile.tile_type == 'acute' else obtuse_color
        else:  # orientation-based
            idx = get_tile_orientation_index(tile)
            hue = idx / 10.0
            face_colors[i] = np.array(colorsys.hsv_to_rgb(
                hue, 0.9, 0.9), dtype=np.float32)

    # Create optimized collection
    collection = PolyCollection(
        vertices,
        facecolors=face_colors,
        edgecolors='black',
        linewidths=0.3,
        closed=True
    )
    ax.add_collection(collection)

    # Auto-scale view
    all_vertices = vertices.reshape(-1, 2)
    min_x, max_x = np.min(all_vertices[:, 0]), np.max(all_vertices[:, 0])
    min_y, max_y = np.min(all_vertices[:, 1]), np.max(all_vertices[:, 1])
    padding = max((max_x - min_x), (max_y - min_y)) * 0.05
    ax.set_xlim(min_x - padding, max_x + padding)
    ax.set_ylim(min_y - padding, max_y + padding)

    ax.set_aspect('equal')
    ax.set_axis_off()
    plt.tight_layout()

    if output_filename:
        plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    else:
        plt.show()


if __name__ == '__main__':
    print("Optimized Penrose Tiling Generator")

    # User input
    while True:
        try:
            depth = int(input("Enter recursion depth (3-6 recommended): "))
            if depth >= 0:
                break
            print("Depth must be non-negative")
        except ValueError:
            print("Please enter an integer")

    color_mode = input(
        "Color mode? [mono/type/color] (default=color): ").strip().lower() or 'color'

    output_file = input(
        "Output filename (optional, .png/.svg): ").strip()

    # Generate and plot
    initial_tiles = create_initial_triangle_star()
    tiles = iterative_subdivide(initial_tiles, depth)
    plot_triangle_tiling(
        tiles, output_file if output_file else None, color_mode)
