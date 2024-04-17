import pickle
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 5555))
game_state_data_recv = client_socket.recv(4096)
game_state = pickle.loads(game_state_data_recv)
print('receive game state')
# gọi server lấy nước đi
valid_moves_data_recv = client_socket.recv(4096)
valid_moves = pickle.loads(valid_moves_data_recv)
print('receive valid moves')
