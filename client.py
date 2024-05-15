import socket
# sysモジュールは、Pythonが実行されているシステムに関連する情報を取得したり、
# システム特有の操作を行ったりするためのPythonの組み込みモジュールです。
import sys

# TCP/IPソケットを作成します。
# ここでソケットとは、通信を可能にするためのエンドポイントです。
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = '/tmp/socket_file'


# サーバが待ち受けている特定の場所にソケットを接続します。
print('connecting to {}'.format(server_address))

# サーバに接続を試みます。
# 何か問題があった場合、エラーメッセージを表示してプログラムを終了します。
try:
    sock.connect((socket.gethostbyname(socket.gethostname()), 12345))
except socket.error as err:
    print(err)
    # sys.exit()を使うと、Pythonプログラムをすぐに終了することができます。
    # ここでの引数1は、プログラムがエラーで終了したことを示すステータスコードです。
    sys.exit(1)

# サーバに接続できたら、サーバにメッセージを送信します。
try:
    # 送信するメッセージを定義します。
    # ソケット通信ではデータをバイト形式で送る必要があります。
    inputMessage = input('Input message: ').encode()
    print('sending : {}'.format(inputMessage))
    sock.sendall(inputMessage)

    # サーバからの応答を待つ時間を2秒間に設定します。
    # この時間が過ぎても応答がない場合、プログラムは次のステップに進みます。
    sock.settimeout(2)

    # サーバからの応答を待ち、応答があればそれを表示します。
    try:
        while True:
            # サーバからのデータを受け取ります。
            # 受け取るデータの最大量は32バイトとします。
            data = str(sock.recv(32))
            print('Received from server: ' + data)
            # データがあればそれを表示し、なければループを終了します。
            if data:
                print('Server response: ' + data)
            else:
                break

    # 2秒間サーバからの応答がなければ、タイムアウトエラーとなり、エラーメッセージを表示します。
    except(TimeoutError):
        print('Socket timeout, ending listening for server messages')

# すべての操作が完了したら、最後にソケットを閉じて通信を終了します。
finally:
    print('closing socket')
    sock.close()
