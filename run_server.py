from waitress import serve
import dashboard  
if __name__ == '__main__':
    serve(dashboard.app.server, host='0.0.0.0', port=8080)
