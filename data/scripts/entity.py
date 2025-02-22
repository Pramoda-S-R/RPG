import json

FACING = {'down': 0, 'left': 4, 'right': 8, 'up': 12}

class Entity():
    def __init__(self, sprite, sprite_map, tile_size, column, facing, keyframe):
        self.sprite = sprite
        try:
            with open(sprite_map) as f:
                self.sprite_map = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading sprite map {sprite_map}: {e}")
            self.sprite_map = {'layers': []}
        self.tile_width, self.tile_height = tile_size
        self.column = column
        self.facing = facing
        self.keyframe = keyframe


    def render_entity(self, screen, facing, keyframe, pos):
        if self.facing not in FACING:
            print(f"Invalid facing direction: {self.facing}")
            return
    
        for layer in self.sprite_map['layers']:
            if layer['id'] == FACING[facing]:
                tile_id = layer['data'][keyframe] - 1
                if tile_id >= 0:  # -1 indicates no tile
                    tile_x = (tile_id % self.column) * self.tile_width
                    tile_y = (tile_id // self.column) * self.tile_height
                    screen.blit(self.sprite, (pos['x'], pos['y']), (tile_x, tile_y, self.tile_width, self.tile_height))


if __name__ == "__main__":
    Entity(None,'data\\characters\\player.json',32,4).render_entity(None, 'down', 1, {'x': 0, 'y': 0})