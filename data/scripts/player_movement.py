class PlayerMovement:
    def __init__(self, player, background, tilesize, camera_speed, moving, camera):
        self.player = player
        self.background = background
        self.tilesize = tilesize
        self.camera_speed = camera_speed
        self.moving = moving
        self.camera = camera
        self.target_camera = camera.copy()

    def move_player(self, direction):
        dx, dy = 0, 0
        if direction == "up":
            dy -= self.tilesize
        elif direction == "left":
            dx -= self.tilesize
        elif direction == "down":
            dy += self.tilesize
        elif direction == "right":
            dx += self.tilesize
        
        if direction:
            self.player.facing = direction

        # Centre camera to player
        target_x = self.target_camera['x'] + dx + (self.tilesize * 7)
        target_y = self.target_camera['y'] + dy + (self.tilesize * 5) + (self.tilesize // 2) 

        # Convert target camera position back to tile coordinates to check for collision
        target_tile_x = target_x // self.tilesize
        target_tile_y = target_y // self.tilesize

        if self.background.is_tile_collidable(target_tile_x, target_tile_y) and (dx, dy) != (0, 0):
            self.target_camera['x'] += dx
            self.target_camera['y'] += dy
            self.moving = True

        # Smoothly move the camera to the target position
        if self.camera['x'] < self.target_camera['x']:
            self.camera['x'] += min(self.camera_speed, self.target_camera['x'] - self.camera['x'])
            self.player.keyframe = int((self.target_camera['x'] - self.camera['x']) / (self.player.column % 6)) % self.player.column
        elif self.camera['x'] > self.target_camera['x']:
            self.camera['x'] -= min(self.camera_speed, self.camera['x'] - self.target_camera['x'])
            self.player.keyframe = int((self.target_camera['x'] - self.camera['x']) / (self.player.column % 6)) % self.player.column
        
        if self.camera['y'] < self.target_camera['y']:
            self.camera['y'] += min(self.camera_speed, self.target_camera['y'] - self.camera['y'])
            self.player.keyframe = int((self.target_camera['y'] - self.camera['y']) / (self.player.column % 6)) % self.player.column
        elif self.camera['y'] > self.target_camera['y']:
            self.camera['y'] -= min(self.camera_speed, self.camera['y'] - self.target_camera['y'])
            self.player.keyframe = int((self.target_camera['y'] - self.camera['y']) / (self.player.column % 6)) % self.player.column

        # Check if the movement is completed
        if self.camera['x'] == self.target_camera['x'] and self.camera['y'] == self.target_camera['y'] and self.moving:
            self.player.keyframe = 0
            self.moving = False
