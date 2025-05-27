import flet as ft
from database import Database

def main(page: ft.Page):
    page.title = "Приложение для контактов"
    page.window_width = 1024
    
    db = Database("contacts.sqlite3")
    db.create_tables()
    
    def get_rows() -> list[ft.Row]:
        rows = []
        for contact in db.all_contacts():
            rows.append(
                ft.Row(
                    controls=[
                        ft.Text(f"{contact[1]} | {contact[2]} | {contact[3]}", expand=True),
                        ft.IconButton(
                            icon=ft.Icons.DELETE, 
                            on_click=delete_contact, 
                            data=contact[0],
                            tooltip="Удалить контакт"
                        ),
                    ]
                )
            )
        return rows
    
    def add_contact(e):
        # Проверяем, что имя и телефон не пустые
        if not name_input.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("Введите имя контакта!"))
            page.snack_bar.open = True
            page.update()
            return
            
        if not phone_input.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("Введите номер телефона!"))
            page.snack_bar.open = True
            page.update()
            return
        
        db.add_contact(
            name=name_input.value.strip(), 
            phone=phone_input.value.strip(), 
            note=note_input.value.strip()
        )
        
        # Обновляем список контактов
        contact_list.controls = get_rows()
        
        # Очищаем поля ввода
        name_input.value = ""
        phone_input.value = ""
        note_input.value = ""
        
        page.update()
    
    def delete_contact(e):
        db.delete_contact(contact_id=e.control.data)
        contact_list.controls = get_rows()
        page.update()
    
    # Создаем элементы интерфейса
    title = ft.Text(value="Контакты", size=33)
    name_input = ft.TextField(label="Имя контакта", width=200)
    phone_input = ft.TextField(label="Телефон", width=200)
    note_input = ft.TextField(label="Примечание", width=200)
    
    add_button = ft.ElevatedButton(text="Добавить", on_click=add_contact)
    form_area = ft.Row(
        controls=[name_input, phone_input, note_input, add_button],
        alignment=ft.MainAxisAlignment.START
    )
    
    contact_list = ft.Column(
        controls=get_rows(), 
        scroll=ft.ScrollMode.AUTO,
        height=400
    )
    
    page.add(title, form_area, contact_list)

ft.app(main)
