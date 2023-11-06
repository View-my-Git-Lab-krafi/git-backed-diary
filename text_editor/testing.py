def choose_file(md_files):
    #app = QApplication([])

    choose_root = QWidget()
    choose_root.setWindowTitle("Select File")
    choose_root.setGeometry(100, 100, 700, 700)

    layout = QVBoxLayout()

    list_widget = QListWidget()
    list_widget.setFixedWidth(400)
    list_widget.setFixedHeight(400)
    font = QFont()
    font.setPointSize(20)
    #font.setBold(True) 

    filtered_files = []
    file_dict = {}

    for file in md_files:
        #list_widget.addItem(file)  # Get with Full path
        if file.endswith('.enc.GitDiarySync'):
            filename = file.split("/")[-1]
            filtered_files.append(filename)
            list_widget.addItem(filename)  # Add only the file name
            file_dict[filename] = file

    print("md_files:", md_files)
    print("filtered_files:", filtered_files)
    print("File Dictionary:", file_dict)

        


    layout.addWidget(list_widget)

    select_button = QPushButton("Select")
    layout.addWidget(select_button)

    selected_file = None 

    def on_select():
        nonlocal selected_file
        selected_file_name = list_widget.selectedItems()[0].text()
        selected_file = file_dict.get(selected_file_name, None)
        if selected_file is None:
            QMessageBox.warning(choose_root, "Warning", "File not found.")
        else:
            choose_root.close()

    select_button.clicked.connect(on_select)
    choose_root.setLayout(layout)

    choose_root.show()
    app.exec_()
    
    print(selected_file)
    return selected_file