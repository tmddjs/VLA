from typing import BinaryIO, List, Union
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

# Ensure Korean labels are rendered correctly
rcParams['font.family'] = 'NanumGothic'

from .layout import PlantLayout
from .grid import Grid


def plot_layout(layout: PlantLayout, image_path: Union[str, BinaryIO]):
    grid = layout.grid
    exposures = grid.exposures
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(exposures, origin='lower', cmap='YlOrRd', extent=[0, grid.width, 0, grid.height])
    for plant, x, y in layout.placements:
        ax.plot(x, y, 'go')
        ax.text(x, y, plant.kr_name or plant.scientific_name, fontsize=6)
    ax.set_xlim(0, grid.width)
    ax.set_ylim(0, grid.height)
    ax.set_xlabel('m')
    ax.set_ylabel('m')
    fig.colorbar(im, ax=ax, label='Light level')
    plt.tight_layout()
    # ``image_path`` may be a filesystem path or a file-like object.  Explicitly
    # specify the format so in-memory buffers are handled correctly.
    plt.savefig(image_path, format="png")
    plt.close(fig)
