from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from fpdf import FPDF, XPos, YPos
from datetime import datetime
from routes.index import index_bp
import os
from model import db
import base64
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath('uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
base_dir = os.path.abspath(os.path.dirname(__file__))  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'instance/voluntario.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db.init_app(app)
# Registrar Blueprints
app.register_blueprint(index_bp) 



class PDF(FPDF):

    def header(self):
        self.set_font('Helvetica', 'B', 16)  # Define a fonte
        page_width = self.w  # Largura total da página
        text = "Relatório de Folhas de Presença"
        text_width = self.get_string_width(text)  # Calcula a largura do texto
        x_position = (page_width - text_width) / 2  # Calcula a posição x para centralizar

        # Define a posição x manualmente e desenha o texto
        self.set_x(x_position)
        self.cell(0, 15, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)

    def footer(self):
        self.set_y(-15)  # Define a posição vertical do rodapé
        self.set_font('Helvetica', 'I', 8)  # Define a fonte

        # Texto à esquerda: Número da página
        self.set_x(10)  # Define a posição horizontal inicial (esquerda)
        self.cell(0, 10, f'Página {self.page_no()}', new_x=XPos.LEFT, new_y=YPos.TOP)

        # Texto à direita: Copyright
        self.set_x(-50)  # Define a posição horizontal final (direita)
        self.cell(0, 10, '© 2025 Setor Guaxupé', new_x=XPos.RIGHT, new_y=YPos.TOP)

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)  # Correção da fonte
        self.set_fill_color(230, 230, 230)
        self.cell(0, 12, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)  # Correção do ln
        self.ln(5)

    def add_images(self, images):
        target_height = 180
        for img_data in images:
            if img_data.startswith('data:image'):
                try:
                    header, data = img_data.split(',', 1)
                    image_type = header.split(';')[0].split('/')[-1]
                    image_bytes = base64.b64decode(data)
                    filename = f"tmp_{datetime.now().strftime('%Y%m%d%H%M%S')}.{image_type}"
                    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    with open(save_path, 'wb') as f:
                        f.write(image_bytes)
                    self.image(save_path, x=10, w=self.w-20, h=target_height)
                    self.ln(target_height + 10)
                    os.remove(save_path)
                except Exception as e:
                    self.cell(0, 10, f'[Erro na imagem: {str(e)}]', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            else:
                self.image(img_data, x=10, w=self.w-20, h=target_height)
                self.ln(target_height + 10)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    house = request.form.get('house')
    month = request.form.get('month')
    days = request.form.get('days')
        # Inverte a ordem de Mês/Ano
     # Mapeamento dos meses em português
    months_pt = {
        "01": "Janeiro",
        "02": "Fevereiro",
        "03": "Março",
        "04": "Abril",
        "05": "Maio",
        "06": "Junho",
        "07": "Julho",
        "08": "Agosto",
        "09": "Setembro",
        "10": "Outubro",
        "11": "Novembro",
        "12": "Dezembro"
    }    
        
        
        
    if month:
            year, month_number = month.split('-')  # Divide em ano e mês
            month_name = months_pt.get(month_number, "Mês inválido")  # Obtém o nome do mês em português
            formatted_month = f"{month_name}/{year}"  # Formato desejado: Mês/Ano
    else:
            formatted_month = "Mês não informado"
    
    categories = []
    for key in request.form:
        if key.startswith('category_name_'):
            idx = key.split('_')[-1]
            images = []
            
            # Processa imagens de upload
            file_images = request.files.getlist(f'category_images_{idx}')
            for img in file_images:
                if img.filename:
                    filename = secure_filename(img.filename)
                    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    img.save(save_path)
                    images.append(save_path)
            
            # Processa imagens capturadas
            captured_images = request.form.get(f'captured_images_{idx}', '[]')
            captured_images = captured_images if captured_images.strip() else '[]'
            images.extend(json.loads(captured_images))
            
            categories.append({
                'name': request.form[key],
                'images': images
            })
    
    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, f"Casa de Oração: {house}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Mês de Competência: {formatted_month}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Período: {days}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Linha abaixo dos dados
    pdf.ln(10)
    
    for category in categories:
        pdf.chapter_title(category['name'])
        pdf.add_images(category['images'])
    
    filename = f"Relatorio_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf.output(pdf_path)
    
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)