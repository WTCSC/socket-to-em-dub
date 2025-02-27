# Traditional Checkers
A multiplayer implementation of the classic Checkers game in Python, allowing two players to compete against each other over a network connection.


## Features
- Standard Checkers rules implementation
- Turn-based multiplayer gameplay
- King piece promotion system
- Piece capturing mechanics
- Network play support

## Requirement
- Python 3.7 of higher
#### You can install this by going to the offical Python website and choose `Windows x86-64 MSI installer`
- Colorama package
#### You can install this by going to a terminal and type in the following `-m pip install colorama`
1. **Install Python**
   - Download from [Python's official website](https://www.python.org/downloads/)
   - Select `Windows x86-64 MSI installer` for Windows

2. **Install Colorama**
   ```bash
   python -m pip install colorama
   ```

3. **Clone the Repository**
   ```bash
   git clone git@github.com:WTCSC/socket-to-em-dub.git
   cd socket-to-em-dub
   ```

## Steps
1. Navigate to the project directory

`cd socket-to-em-dub`

2. Run the game

`python3 server.py` or `python3 client.py`

**Server**

3. Enter any port number (We suggest anything above 5000)

**EX.** Enter port to host the game on: `5000`

**Client**

3. Enter the server ip (you can find it by using `ipconfig` on the server device commadn terminal)

**EX.** Enter server IP: 127.0.0.1

4. Enter the port that is hosted on the server

**EX.** Enter server port: `5000`

## Controls

- Enter moves in the format: `from_row,from_col to_row,to_col`
- Example move: `5,0 4,1`
- Type `q` to quit the game