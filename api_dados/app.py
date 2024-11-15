from flask import Flask, render_template, request, flash
from config import Config
from database_service import get_all_records, insert_record, update_record, delete_record
from plot_service import create_graphs

app = Flask(__name__)
app.config.from_object(Config)

# Rota INDEX
@app.route('/')
def index():
    return render_template('index.html')

# Rotas GET
@app.route('/get_options', methods=['GET'])
def get_options():
    data = get_all_records()
    return render_template('get_options.html', data=data)

# Rota Gráfico
@app.route('/graph', methods=['GET'])
def graph():
    graph_path = create_graphs()
    return render_template('graph.html', graph_path=graph_path)

# Rotas POST
@app.route('/post_options', methods=['GET', 'POST'])
def post_options():
    if request.method == 'POST':
        data = request.form.to_dict()
        insert_record(data)
        flash("Registro adicionado com sucesso!", "success")
        return render_template('post_options.html')
    
    return render_template('post_options.html')

# Rotas PUT
@app.route('/put_options', methods=['GET', 'POST'])
def put_options():
    if request.method == 'POST':
        record_id = request.form.get("id")
        new_data = request.form.to_dict()
        update_record(record_id, new_data)
        flash("Registro atualizado com sucesso!", "success")
        return render_template('put_options.html')

    return render_template('put_options.html')

# Rotas DELETE
@app.route('/delete_options', methods=['GET', 'POST'])
def delete_options():
    if request.method == 'POST':
        record_id = request.form.get("id")
        delete_record(record_id)
        flash("Registro excluído com sucesso!", "success")
        return render_template('delete_options.html')

    return render_template('delete_options.html')

if __name__ == '__main__':
    app.run(debug=True)
