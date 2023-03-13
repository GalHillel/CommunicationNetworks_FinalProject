import tkinter as tk
import socket


# define function to initiate connection
def connect():
    # get inputs from GUI
    global clientsocket
    url = url_input.get().strip()
    protocol = protocol_var.get()
    filename = filename_input.get().strip()

    # check if URL and filename are not empty
    if not url or not filename:
        response_label.config(text='Please provide a valid URL and filename')
        return

    # get local machine name
    host = socket.gethostname()

    # define port numbers for TCP and RUDP
    tcp_port = 9898
    rudp_port = 7878

    # create a socket object for the chosen protocol
    if protocol.upper() == 'TCP':
        sock_type = socket.SOCK_STREAM
        port = tcp_port
    elif protocol.upper() == 'RUDP':
        sock_type = socket.SOCK_DGRAM
        port = rudp_port
    else:
        response_label.config(text='Invalid protocol choice')
        return

    try:
        clientsocket = socket.socket(socket.AF_INET, sock_type)

        # connect to the server
        clientsocket.connect((host, port))

        # send URL and filename to server
        message = f"{url},{filename}"
        clientsocket.sendto(message.encode('utf-8'), (host, port))

        # receive response from server
        response, server_address = clientsocket.recvfrom(1024)

        # update GUI with response
        response_label.config(text=response.decode('utf-8'))

    except Exception as e:
        response_label.config(text=f"Error: {e}")
    finally:
        # close the socket
        clientsocket.close()


# create GUI
root = tk.Tk()
root.title('HTTP Downloader')
root.geometry('400x300')

# create label for URL input field
url_label = tk.Label(root, text='URL:')
url_label.pack(pady=10)

# create URL input field
url_input = tk.Entry(root, width=30)
url_input.pack()

# create label for protocol selection
protocol_label = tk.Label(root, text='Protocol:')
protocol_label.pack(pady=10)

# create protocol selection radio buttons
protocol_var = tk.StringVar()
tcp_rb = tk.Radiobutton(root, text='TCP', variable=protocol_var, value='TCP')
rudp_rb = tk.Radiobutton(root, text='RUDP', variable=protocol_var, value='RUDP')
tcp_rb.pack()
rudp_rb.pack()

# create label for filename input field
filename_label = tk.Label(root, text='Filename:')
filename_label.pack(pady=10)

filename_input = tk.Entry(root, width=30)
filename_input.pack()

# create button to initiate connection
connect_button = tk.Button(root, text='Download', command=connect)
connect_button.pack(pady=20)

# create label for response
response_label = tk.Label(root, text='')
response_label.pack()

root.mainloop()