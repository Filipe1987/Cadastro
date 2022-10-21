from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import sqlite3
import pandas as pd
from sqlite3 import Error


conexao = sqlite3.connect('banco_diaconato.db')

c = conexao.cursor()

# c.execute("""  CREATE TABLE diaconato
# (
#     id integer NOT NULL,
#     nome text,
#     lider text,
#     coord text,
#     funcao text,
#     email text,
#     telefone text,
#     data text,
#     PRIMARY KEY("id" AUTOINCREMENT)
#
# )
#   """ )


conexao.commit()

conexao.close()

lista_lideres = ['Carlos Jervan', 'Gigi', 'Odirlei Grigório', 'Silvia Soares', 'Amilton Xavier', 'Jeovan Geraldo',
                 'Heitor de Melo', 'Silvia Correia', 'Marli', 'Alex Santos', 'Ederson Vieira', 'Lourdes Sabino', 'Denise Mendes',
                 'Rose', 'Vânia' ]


lista_coord = ['Emerson Amaro', 'Tatiane Macedo', 'Telma Rezende', 'Leandro dos Santos', 'Taís Marques',
               'Luiz Carlos', 'Ester Lopes']

lista_funcoes = ['Cooperador', 'Diácono', 'Voluntário', 'Líder', 'Coordenador']




def cadastrar_membro():
    """Não permitir linhas em branco no Cadastro"""
    if entry_nome.get() == "" or entry_lider.get() == "" or entry_coord.get() == "" or entry_funcao.get() == "" or entry_email.get() == "" or entry_telefone.get() == "" or entry_data.get() == "":
        messagebox.showerror(title="Erro no preenchimento", message="Campos em branco")


    else:
        try:
            conexao = sqlite3.connect('banco_diaconato.db')

            c = conexao.cursor()

            c.execute("INSERT INTO diaconato VALUES(:id, :nome, :lider, :coord, :funcao, :email, :telefone, :data )",
                      {
                          'id': None,
                          'nome': entry_nome.get(),
                          'lider': entry_lider.get(),
                          'coord': entry_coord.get(),
                          'funcao': entry_funcao.get(),
                          'email': entry_email.get(),
                          'telefone': entry_telefone.get(),
                          'data': entry_data.get()

                      }
                      )

            conexao.commit()

            conexao.close()

            entry_nome.delete(0, "end")
            entry_lider.delete(0, "end")
            entry_coord.delete(0, "end")
            entry_funcao.delete(0, "end")
            entry_email.delete(0, "end")
            entry_telefone.delete(0, "end")
            entry_data.delete(0, "end")

            messagebox.showinfo(title="Sucesso!!", message="Cadastro Realizado com Sucesso!!")

        except:
            messagebox.showerror(title="Erro Servidor", message="Falta de conexão com o Banco")





def ConexaoBanco():
    conexao=None
    try:
        conexao = sqlite3.connect('banco_diaconato.db')
    except Error as ex:
        print((ex))
    return conexao


def dql(query):
    conexao = sqlite3.connect('banco_diaconato.db')

    c = conexao.cursor()

    c.execute(query)

    res=c.fetchall()

    conexao.close()

    return res


def dml(query):
    try:
        conexao = sqlite3.connect('banco_diaconato.db')

        c = conexao.cursor()

        c.execute(query)

        conexao.commit()

        conexao.close()

    except Error as ex:
        print(ex)


def popular():
    tv.delete(*tv.get_children())
    conexao = sqlite3.connect('banco_diaconato.db')

    c = conexao.cursor()

    linhas = c.execute("SELECT * FROM diaconato order by nome")

    for i in linhas:
        tv.insert("", "end", values=i)


    conexao.close()


def popular2():
    tv2.delete(*tv2.get_children())
    conexao = sqlite3.connect('banco_diaconato.db')

    c = conexao.cursor()

    linhas = c.execute("SELECT * FROM diaconato order by nome")

    for i in linhas:
        tv2.insert("", "end", values=i)

    conexao.close()


def exportar_excel():
    conexao = sqlite3.connect('banco_diaconato.db')

    c = conexao.cursor()

    c.execute("SELECT *, oid FROM diaconato ")
    diaconos_cadastrados = c.fetchall()
    diaconos_cadastrados = pd.DataFrame(diaconos_cadastrados, columns=['nome', 'lider', 'coord', 'funcao', 'email', 'telefone', 'data', 'ID'])
    diaconos_cadastrados.to_excel('Cadastro Diaconos.xlsx')
    conexao.commit()

    conexao.close()

def exportar_pdf():
    pass


def pesquisa():
    tv.delete(*tv.get_children())
    c = "SELECT * from diaconato WHERE nome LIKE '%"+entry_pesquisar.get()+"%'"
    linhas = dql(c)
    for i in linhas:
        tv.insert("", "end", values=i)

def pesquisa_grupos():
    tv2.delete(*tv2.get_children())
    c = "SELECT * from diaconato WHERE coord LIKE '%" + vcoord.get() + "%'"
    linhas = dql(c)
    for i in linhas:
        tv2.insert("", "end", values=i)

def deletar():
    res = messagebox.askyesno(title="Deletar Registro", message="Certeza que deseja deletar o registro?")
    if(res == True):
        vid = -1
        itemSelecionado = tv.selection()[0]
        valores = tv.item(itemSelecionado, "values")
        vid = valores[0]
        print(vid)
        try:
            vquery = "DELETE FROM diaconato WHERE id=" + vid
            dml(vquery)

        except:
            messagebox.showerror(title="ERRO", message="Erro ao deletar")
            return
        tv.delete(itemSelecionado)

    else:
        messagebox.showinfo(title="Cancelado", message="Registro não foi deletado!!")

def pesquisa_id():
   pass




inicial = Tk()
inicial.title("Home - Banco de Dados Diaconato")
inicial.geometry("720x500")
inicial.configure(background='#3366FF')
inicial.resizable(False, False)
inicial.iconbitmap("imagens/icon.ico")

vcoord = StringVar()

nb = ttk.Notebook(inicial)
nb.place(x=0, y=0, width=720, height=500)


"""Códigos da Área de Cadastro"""
tb1 = Frame(nb, background='#3366FF')


#Labels

# label_titulo = Label(cadastro, text="Cadastro Diáconos e Voluntários", font="Times 20 bold", bg='#3366FF')
# label_titulo.pack


label_nome  = tk.Label(tb1, text='Nome', background='#3366FF', anchor = W)
label_nome.grid(row=1 , column=0, padx=10, pady=10)
label_nome.configure(font=16)

label_lider  = tk.Label(tb1, text='Lider', background='#3366FF',  anchor = W)
label_lider.grid(row=2 , column=0, padx=10, pady=10)
label_lider.configure(font=16)

label_coord  = tk.Label(tb1, text='Coordenador', background='#3366FF',  anchor = W)
label_coord.grid(row=3 , column=0, padx=10, pady=10)
label_coord.configure(font=16)

label_funcao  = tk.Label(tb1, text='Função', background='#3366FF', anchor = W)
label_funcao.grid(row=4 , column=0, padx=10, pady=10)
label_funcao.configure(font=16)

label_email  = tk.Label(tb1, text='E-mail', background='#3366FF', anchor = W)
label_email.grid(row=5 , column=0, padx=10, pady=10)
label_email.configure(font=16)

label_telefone  = tk.Label(tb1, text='Telefone', background='#3366FF', anchor = W)
label_telefone.grid(row=6 , column=0, padx=10, pady=10)
label_telefone.configure(font=16)

label_data  = tk.Label(tb1, text='Data', background='#3366FF', anchor = W)
label_data.grid(row=7 , column=0, padx=10, pady=10)
label_data.configure(font=16)



#Entry e Combobox

entry_nome = tk.Entry(tb1, width=50)
entry_nome.grid(row=1 , column=1, padx=0, pady=10)
entry_nome.configure(font=16)

entry_lider = ttk.Combobox(tb1, value=lista_lideres, width=45)
entry_lider.grid(row=2 , column=1, padx=0, pady=10)
entry_lider.configure(font=16)

entry_coord = ttk.Combobox(tb1, value=lista_coord, width=45)
entry_coord.grid(row=3 , column=1, padx=0, pady=10)
entry_coord.configure(font=16)

entry_funcao = ttk.Combobox(tb1, value=lista_funcoes, width=45)
entry_funcao.grid(row=4 , column=1, padx=0, pady=10)
entry_funcao.configure(font=16)

entry_email = tk.Entry(tb1, width=50)
entry_email.grid(row=5 , column=1, padx=0, pady=10)
entry_email.configure(font=16)

entry_telefone = tk.Entry(tb1, width=30)
entry_telefone.grid(row=6 , column=1, padx=0, pady=10)
entry_telefone.configure(font=16)

entry_data = tk.Entry(tb1, width=20)
entry_data.grid(row=7 , column=1, padx=0, pady=10)
entry_data.configure(font=16)



#Botôes

botao_cadastrar  = tk.Button(tb1, text='Cadastrar Novo Diácono', command = cadastrar_membro, width=40)
botao_cadastrar.grid(row=8 , column=1, padx=0, pady=10, ipadx = 20)

botao_exportar  = tk.Button(tb1, text='Criar Planilha', command = exportar_excel)
botao_exportar.grid(row=8 , column=0, padx=10, pady=10, ipadx = 20)

botao_alterar  = tk.Button(tb1, text='Alterar Cadastro', command = exportar_pdf(), width=40)
botao_alterar.grid(row=9 , column=1, padx=0, pady=10, ipadx = 20)

botao_alterar  = tk.Button(tb1, text='Deletar Cadastro', command = exportar_pdf(), width=40)
botao_alterar.grid(row=10 , column=1, padx=0, pady=10, ipadx = 20)

botao_exportar  = tk.Button(tb1, text='Criar PDF', command = exportar_pdf)
botao_exportar.grid(row=9 , column=0, padx=10, pady=10, ipadx = 20)

nb.add(tb1, text="Cadastro")
####################################################################################################

tb2 = Frame(nb, background='#3366FF')

quadroGrid = LabelFrame(tb2, text='Informações')
quadroGrid.pack(fill="both", expand='yes', padx=10, pady=10)

tv = ttk.Treeview(quadroGrid, columns=('ID', 'Nome', 'Lider', 'Coordenador', 'Função', 'E-mail', 'Telefone', 'Data'), show='headings')
tv.column('ID', minwidth=0, width=20)
tv.column('Nome', minwidth=0, width=100)
tv.column('Lider', minwidth=0, width=100)
tv.column('Coordenador', minwidth=0, width=100)
tv.column('Função', minwidth=0, width=80)
tv.column('E-mail', minwidth=0, width=150)
tv.column('Telefone', minwidth=0, width=80)
tv.column('Data', minwidth=0, width=100)
tv.heading('ID', text="ID")
tv.heading('Nome', text='Nome')
tv.heading('Lider', text='Lider')
tv.heading('Coordenador', text='Coord')
tv.heading('Função', text='Função')
tv.heading('E-mail', text='E-mail')
tv.heading('Telefone', text='Telefone')
tv.heading('Data', text='Data')
tv.pack()
popular()

nb.add(tb2, text="Geral")

quadroGrid2 = LabelFrame(tb2, text='Informações')
quadroGrid2.pack(fill="both", expand='yes', padx=10, pady=10)

label_nomep  = tk.Label(quadroGrid2, text='Nome para a pesquisa', anchor = W).pack()

entry_pesquisar = tk.Entry(quadroGrid2, width=50)
entry_pesquisar.pack()


botao_pesquisar = tk.Button(quadroGrid2, text='Pesquisar', command=pesquisa, width=40).pack()
botao_deletar = tk.Button(quadroGrid2, text='Deletar', command=deletar, width=40).pack()

botao_atualizar = tk.Button(quadroGrid2, text='Mostrar Todos', command=popular, width=40).pack()
##############################################################################################################

tb3 = Frame(nb, background='#3366FF')

quadroGrid1 = LabelFrame(tb3, text='Grupos')
quadroGrid1.pack(fill="both", expand='yes', padx=10, pady=10)

coor_tati = Radiobutton(quadroGrid1, text="Tatiane Macedo", value=lista_coord[1], command=pesquisa_grupos, variable=vcoord)
coor_tati.grid(row=0 , column=1, padx=0, pady=10)

coor_emerson = Radiobutton(quadroGrid1, text="Emerson Amaro", value=lista_coord[0], command=pesquisa_grupos, variable=vcoord)
coor_emerson.grid(row=0 , column=2, padx=0, pady=10)

coor_telma = Radiobutton(quadroGrid1, text="Telma Rezende", value=lista_coord[2], command=pesquisa_grupos, variable=vcoord)
coor_telma.grid(row=0 , column=3, padx=0, pady=10)

coor_leandro = Radiobutton(quadroGrid1, text="Leandro dos Santos", value=lista_coord[3], command=pesquisa_grupos, variable=vcoord)
coor_leandro.grid(row=0 , column=4, padx=0, pady=10)

coor_luiz = Radiobutton(quadroGrid1, text="Luiz Carlos", value=lista_coord[5], command=pesquisa_grupos, variable=vcoord)
coor_luiz.grid(row=1 , column=1, padx=0, pady=10)

coor_tais = Radiobutton(quadroGrid1, text="Taís Marques", value=lista_coord[4], command=pesquisa_grupos, variable=vcoord)
coor_tais.grid(row=1 , column=2, padx=0, pady=10)

coor_ester = Radiobutton(quadroGrid1, text="Ester Lopes", value=lista_coord[6], command=pesquisa_grupos, variable=vcoord)
coor_ester.grid(row=1 , column=3, padx=0, pady=10)

quadroGrid3 = LabelFrame(tb3, text='Filtro')
quadroGrid3.pack(fill="both", expand='yes', padx=10, pady=10)

tv2 = ttk.Treeview(quadroGrid3, columns=('ID', 'Nome', 'Lider', 'Coordenador', 'Função', 'E-mail', 'Telefone', 'Data'), show='headings')
tv2.column('ID', minwidth=0, width=20)
tv2.column('Nome', minwidth=0, width=100)
tv2.column('Lider', minwidth=0, width=100)
tv2.column('Coordenador', minwidth=0, width=100)
tv2.column('Função', minwidth=0, width=80)
tv2.column('E-mail', minwidth=0, width=150)
tv2.column('Telefone', minwidth=0, width=80)
tv2.column('Data', minwidth=0, width=100)
tv2.heading('ID', text="ID")
tv2.heading('Nome', text='Nome')
tv2.heading('Lider', text='Lider')
tv2.heading('Coordenador', text='Coord')
tv2.heading('Função', text='Função')
tv2.heading('E-mail', text='E-mail')
tv2.heading('Telefone', text='Telefone')
tv2.heading('Data', text='Data')
tv2.pack()
popular2()


nb.add(tb3, text="Grupos")

#####################################################################################################################
tb4 = Frame(nb, background='#3366FF')
nb.add(tb4, text="Relatório")

tb5 = Frame(nb, background='#3366FF')
nb.add(tb5, text="Alterar")

label_id  = tk.Label(tb5, text='ID', background='#3366FF', anchor = W)
label_id.grid(row=1 , column=0, padx=10, pady=10)
label_id.configure(font=16)

label_nome  = tk.Label(tb5, text='Nome', background='#3366FF', anchor = W)
label_nome.grid(row=2 , column=0, padx=10, pady=10)
label_nome.configure(font=16)

label_lider  = tk.Label(tb5, text='Lider', background='#3366FF',  anchor = W)
label_lider.grid(row=3 , column=0, padx=10, pady=10)
label_lider.configure(font=16)

label_coord  = tk.Label(tb5, text='Coordenador', background='#3366FF',  anchor = W)
label_coord.grid(row=4 , column=0, padx=10, pady=10)
label_coord.configure(font=16)

label_funcao  = tk.Label(tb5, text='Função', background='#3366FF', anchor = W)
label_funcao.grid(row=5 , column=0, padx=10, pady=10)
label_funcao.configure(font=16)

label_email  = tk.Label(tb5, text='E-mail', background='#3366FF', anchor = W)
label_email.grid(row=6 , column=0, padx=10, pady=10)
label_email.configure(font=16)

label_telefone  = tk.Label(tb5, text='Telefone', background='#3366FF', anchor = W)
label_telefone.grid(row=7 , column=0, padx=10, pady=10)
label_telefone.configure(font=16)

label_data  = tk.Label(tb5, text='Data', background='#3366FF', anchor = W)
label_data.grid(row=8 , column=0, padx=10, pady=10)
label_data.configure(font=16)

entry_id = tk.Entry(tb5, width=10)
entry_id.grid(row=1 , column=1, padx=0, pady=10)
entry_id.configure(font=16)

entry_nome5 = tk.Entry(tb5, width=40)
entry_nome5.grid(row=2 , column=1, padx=0, pady=10)
entry_nome5.configure(font=16)

entry_lider5 = ttk.Combobox(tb5, value=lista_lideres, width=40)
entry_lider5.grid(row=3 , column=1, padx=0, pady=10)
entry_lider5.configure(font=16)

entry_coord5 = ttk.Combobox(tb5, value=lista_coord, width=40)
entry_coord5.grid(row=4 , column=1, padx=0, pady=10)
entry_coord5.configure(font=16)

entry_funcao5 = ttk.Combobox(tb5, value=lista_funcoes, width=40)
entry_funcao5.grid(row=5 , column=1, padx=0, pady=10)
entry_funcao5.configure(font=16)

entry_email5 = tk.Entry(tb5, width=40)
entry_email5.grid(row=6 , column=1, padx=0, pady=10)
entry_email5.configure(font=16)

entry_telefone5 = tk.Entry(tb5, width=30)
entry_telefone5.grid(row=7 , column=1, padx=0, pady=10)
entry_telefone5.configure(font=16)

entry_data5 = tk.Entry(tb5, width=10)
entry_data5.grid(row=8 , column=1, padx=0, pady=10)
entry_data5.configure(font=16)

botao_pesquisa_id  = tk.Button(tb5, text='Pesquisar ID', command = pesquisa_id, width=10)
botao_pesquisa_id.grid(row=1 , column=2, padx=0, pady=10, ipadx = 20)



inicial.mainloop()