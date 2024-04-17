import pickle
import socket
import threading
import chess_engine

clients = []


def socket_handle(server_socket, client_address, turn):
    print("Kết nối từ:", client_address, turn)
    game_state_dict = {'game_state': chess_engine.GameState(), 'turn': turn}
    game_state_data = pickle.dumps(game_state_dict)
    game_state = game_state_dict['game_state']
    server_socket.sendall(game_state_data)
    print(client_address, ": sent game state")
    valid_moves = game_state.getValidMoves()  # ds nước đi hợp lệ hiện tại
    send_valid_moves(server_socket, valid_moves)
    while True:
        player_request_data = server_socket.recv(4096)
        if player_request_data:
            player_request = pickle.loads(player_request_data)
            if player_request['type'] == 'click':
                print('Thực hiện nước đi: ', end='')
                player_clicks = player_request['data_click']
                print(player_clicks)
                move = chess_engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                move_made = False
                animate = False
                for i in range(len(valid_moves)):
                    if move == valid_moves[i]:
                        game_state.makeMove(valid_moves[i])
                        move_made = True
                        animate = True
                move_result = {'move_made': move_made, 'animate': animate, 'game_state': game_state}
                move_result_data = pickle.dumps(move_result)
                server_socket.sendall(move_result_data)
                if move_made:
                    valid_moves = game_state.getValidMoves()
                    send_valid_moves(server_socket, valid_moves)
                    # for sc in clients:
                    #     if sc != server_socket:
                    #         my_game_state_data = pickle.dumps(game_state)
                    #         sc.sendall(my_game_state_data)

    # Đóng kết nối với máy khách


def send_valid_moves(server_socket, valid_moves):
    valid_moves_data = pickle.dumps(valid_moves)
    server_socket.sendall(valid_moves_data)
    print(client_address, ": sent valid moves", len(valid_moves))


# Thiết lập máy chủ
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5555))
server.listen()
print("Server đã sẵn sàng để kết nối")

# Chấp nhận kết nối từ các máy khách và tạo luồng xử lý
while True:
    server_socket, client_address = server.accept()
    clients.append(server_socket)
    if clients.index(server_socket) % 2 == 0:
        turn = True
    else:
        turn = False
    client_thread = threading.Thread(target=socket_handle, args=(server_socket, client_address, turn))
    client_thread.start()
