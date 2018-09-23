from flask import render_template
import connexion

app = connexion.App(__name__, specification_dir='./spec')
app.add_api('swagger.yml')

@app.route('/')
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)