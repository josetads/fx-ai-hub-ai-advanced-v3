@echo off
curl http://127.0.0.1:8000/api/v1/rates/collect
curl http://127.0.0.1:8000/api/v1/ml/forecast-all
curl http://127.0.0.1:8000/api/v1/recommendations/all
curl http://127.0.0.1:8000/api/v1/reports/generate
pause
