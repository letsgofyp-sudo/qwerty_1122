@echo off

echo [BUILD] Installing Python dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies
    exit /b %ERRORLEVEL%
)

echo [BUILD] Collecting static files...
python manage.py collectstatic --noinput --clear

if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Failed to collect static files
)

echo [BUILD] Creating necessary directories...
if not exist "staticfiles" mkdir staticfiles
if not exist "media" mkdir media

echo [BUILD] Copying admin static files...
if exist "Lib\site-packages\django\contrib\admin\static\admin" (
    xcopy /E /I /Y "Lib\site-packages\django\contrib\admin\static\admin" "staticfiles\admin"
)

echo [BUILD] Copying app static files...
if exist "administration\static" (
    xcopy /E /I /Y "administration\static" "staticfiles\"
)

if exist "lets_go\static" (
    xcopy /E /I /Y "lets_go\static" "staticfiles\"
)

echo [BUILD] Setting permissions...
icacls "staticfiles" /grant "Everyone:(OI)(CI)F" /T
icacls "media" /grant "Everyone:(OI)(CI)F" /T

echo [BUILD] Build completed successfully
exit 0
