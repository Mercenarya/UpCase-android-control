import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Stack(
            [
                ft.CircleAvatar(
                    content=ft.Icon(name=ft.icons.NOTIFICATIONS),
                    bgcolor="Orange",
                ),
                ft.Container(
                    content=ft.Container(
                        ft.Text("1",color="white",size=10),
                        width=20,
                        height=20,
                        bgcolor="red",
                        border_radius=10,
                        padding=ft.padding.only(left=6,top=3)
                    ),
                    alignment=ft.alignment.bottom_left,
                ),
            ],
            width=40,
            height=40,
        )
    )

ft.app(target=main)