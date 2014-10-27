import rasterio
from rasterio import warp


with rasterio.drivers(CPL_DEBUG=True):
    # Open the source dataset.
    with rasterio.open('/home/vortex/Desktop/LAYERS/MODIS_5600/single_band') as src:
        # Create a destination dataset based on source params. The
        # destination will be tiled, and we'll "process" the tiles
        # concurrently.
        meta = src.meta





warp.reproject('/home/vortex/Desktop/LAYERS/MODIS_5600/single_band', 'test.tiff', 'EPSG:4326', 'EPSG:"3857')