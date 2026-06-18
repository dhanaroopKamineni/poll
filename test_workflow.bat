@echo off
REM Test complete survey and poll workflow

setlocal enabledelayedexpansion

set TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc4MTc2MzkwNn0.xdmBdZmL2HXgIe4UUv6rsaeezNpYco10h6b1JV5Wzgw
set BASE_URL=http://127.0.0.1:8000

echo ========================================
echo Survey & Poll Workflow Test
echo ========================================

echo.
echo 1. List Active Surveys
curl.exe -s -X GET "%BASE_URL%/api/surveys" -H "Authorization: Bearer %TOKEN%" | findstr /R "title|id"

echo.
echo 2. Get Survey Details (ID: 1)
curl.exe -s -X GET "%BASE_URL%/api/surveys/1" -H "Authorization: Bearer %TOKEN%" | findstr /R "title|questions|start_datetime"

echo.
echo 3. Start Survey Session
curl.exe -s -X POST "%BASE_URL%/api/surveys/sessions" -H "Authorization: Bearer %TOKEN%" -H "Content-Type: application/json" -d "{\"survey_id\":1}"

echo.
echo ========================================
echo All tests completed!
echo ========================================
