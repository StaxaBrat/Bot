#!/bin/bash
gunicorn -w 1 -b 0.0.0.0:5000 app:app & python bot.py
#!/bin/sh
gunicorn -w 4 -b 0.0.0.0:$PORT app:app
