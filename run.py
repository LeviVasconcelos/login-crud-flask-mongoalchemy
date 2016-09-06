from movieslib import MoviesLib_app

if __name__ == '__main__':
#   print MoviesLib_app.config['MONGOALCHEMY_CONNECTION_STRING']
   MoviesLib_app.run(host='0.0.0.0',port='8080')
