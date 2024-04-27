import json

class Tilemap():
    def __init__(self, surf, tilemap, tile_size, tileset_columns):
        self.tileset = surf
        with open(tilemap) as f:
            self.tilemap = json.load(f)
        self.tile_size = tile_size
        self.tileset_columns = tileset_columns
        self.collidable_tiles = {2041, -1}


    def is_tile_collidable(self, x, y):
        # Calculate the linear index in the tilemap data array
        index = y * (self.tilemap['layers'][0]['width']) + x
        tile_id = self.tilemap['layers'][0]['data'][index] - 1  # Adjust for Tiled's 1-indexing
        return tile_id in self.collidable_tiles
    

    def render_collisions(self, surf, camera_x, camera_y):
        for layer in self.tilemap['layers']:
                if layer['type'] == 'collision':
                    for y in range(layer['height']):
                        for x in range(layer['width']):
                            tile_id = layer['data'][y * layer['width'] + x] - 1  # Tiled IDs are 1-indexed
                            if tile_id >= 0:  # -1 indicates no tile
                                tile_x = (tile_id % self.tileset_columns) * self.tile_size
                                tile_y = (tile_id // self.tileset_columns) * self.tile_size
                                surf.blit(self.tileset, (x * self.tile_size - camera_x, y * self.tile_size - camera_y - (self.tile_size // 2)), (tile_x, tile_y, self.tile_size, self.tile_size))



    def render_map(self, surf, camera_x, camera_y):
        for layer in self.tilemap['layers']:
            if layer['type'] == 'tilelayer':
                for y in range(layer['height']):
                    for x in range(layer['width']):
                        tile_id = layer['data'][y * layer['width'] + x] - 1  # Tiled IDs are 1-indexed
                        if tile_id >= 0:  # -1 indicates no tile
                            tile_x = (tile_id % self.tileset_columns) * self.tile_size
                            tile_y = (tile_id // self.tileset_columns) * self.tile_size
                            surf.blit(self.tileset, (x * self.tile_size - camera_x, y * self.tile_size - camera_y - (self.tile_size // 2)), (tile_x, tile_y, self.tile_size, self.tile_size))


    def render_foreground(self, surf, camera_x, camera_y):
        for layer in self.tilemap['layers']:
            if layer['type'] == 'foreground':
                for y in range(layer['height']):
                    for x in range(layer['width']):
                        tile_id = layer['data'][y * layer['width'] + x] - 1  # Tiled IDs are 1-indexed
                        if tile_id >= 0:  # -1 indicates no tile
                            tile_x = (tile_id % self.tileset_columns) * self.tile_size
                            tile_y = (tile_id // self.tileset_columns) * self.tile_size
                            surf.blit(self.tileset, (x * self.tile_size - camera_x, y * self.tile_size - camera_y - (self.tile_size // 2)), (tile_x, tile_y, self.tile_size, self.tile_size))