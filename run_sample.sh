osascript -e 'tell app "Terminal"
    do script "cpython3 Node.py 1"
end tell'

osascript -e 'tell app "Terminal"
    do script "python3 Node.py 2"
end tell'

osascript -e 'tell app "Terminal"
    do script "python3 Node.py 3"
end tell'

osascript -e 'tell app "Terminal"
    do script "python3 Client.py 111"
end tell'
