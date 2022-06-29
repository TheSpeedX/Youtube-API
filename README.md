# Youtube-API

## About

This is a Backend Server in FastAPI (Python) that asynchronously scraps latest youtube videos.

The latest scrapped videos include information like -

- Video Id
- Video title
- Video Description
- Channel title
- Publish Time
- Thumbnail URL

These information are stored in the MongoDB Atlas URL configurable via .env file

You can use multiple API Keys to hit API to prevent Quota Usage. Add multiple key in .env separated by space.

API Key can be created in Google Console after Activating Youtube Data V3 API

### Features

- [x] Scraps youtube videos with keyword "official" which can be updated in .env
- [x] Scrap interval is 60 seconds configurable in .env
- [x] Scraps in background
- [x] Multiple API Key Supported

### How To Run

With Docker:  
Make sure docker and docker-compose is installed

```bash
git clone https://github.com/TheSpeedX/Youtube-API
cd Youtube-API
docker-compose up
```

Without Docker:
Make sure Python and PIP is installed

```bash
git clone https://github.com/TheSpeedX/Youtube-API
cd Youtube-API
pip install -r requirements.txt
cd app
uvicorn main:app --host 0.0.0.0 --port 8000
```

Now open <http://127.0.0.1:8000/dashboard> for dashboard <http://127.0.0.1:8000/docs> for docs
