from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):

    """
    For more information on CORS see:
    * https://developer.mozilla.org/en-US/docs/HTTP/Access_control_CORS
    * http://enable-cors.org/
    """
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")

    def do_GET(self):

        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        direction = parsed_qs.get('direction',[None])[0]
        player_x = parsed_qs.get('x', [None])[0]
        player_y = parsed_qs.get('y', [None])[0]

        player_pos = {'x':2,'y':2}

        grid = [
                ['entrance','aisle','aisle','aisle','aisle','facility','facility','facility','wall'],
                ['wall','seat','seat','seat','aisle','seat','seat','seat','wall'],
                ['wall','seat','seat','seat','aisle','seat','seat','seat','wall'],
                ['exit','seat','seat','seat','aisle','seat','seat','seat','exit'],
            ]

        if direction and player_x and player_y:
            
            player_pos = {'x':int(player_x),'y':int(player_y)}

            new_x = player_pos['x']
            new_y = player_pos['y']

            if direction == 'up':
                new_y -= 1
            elif direction == 'down':
                new_y += 1
            elif direction == 'right':
                new_x += 1
            elif direction == 'left':
                new_x -= 1


            valid_move = False

            in_bounds = new_y >= 0 and new_y < len(grid) and new_x >=0 and new_x < len(grid[new_y])

            if in_bounds:
                
                cell = grid[new_y][new_x]

                if cell is 'seat' and new_y is player_pos['y']:
                    valid_move = True
                elif not cell in ('facility','wall'):
                    valid_move = True
                    

            if valid_move:
                player_pos['x'] = new_x
                player_pos['y'] = new_y


        game = {
            'player_pos': player_pos,
            'grid': grid
        }

        message = json.dumps(game)
        
        
        self.wfile.write(message.encode())
        return

