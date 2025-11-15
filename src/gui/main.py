import flet as ft
from src.algoritm import *

def main(page: ft.Page):
    page.title = "Abyss compress"
    page.window.width = 500
    page.window.height = 700
    page.window.min_width = 500
    page.window.min_height = 700
    page.bgcolor = '#2a2a2a'


    def on_compress_click(input_path: str, output_directory: str):
        compressor.compress_file(input_path, output_directory)
    
    def on_decompress_click(input_path: str, output_directory: str):
        decompressor.decompress_file(input_path, output_directory)

    def on_input_close():
        input_path.value = "Select a file to compress"
        page.update()
    
    def on_output_close():
        output_directory.value = "Select a output directory"
        page.update()
    
    def on_filepicker_input(data: ft.FilePickerResultEvent):
        nonlocal input_file_name
        if data.files:
            for file in data.files:
                input_path.value = file.path
                input_file_name = file.name
        page.update()
    
    def on_filepicker_output(data: ft.FilePickerResultEvent):
        if data.path:
            output_directory.value = data.path
        page.update()

    filepicker = ft.FilePicker(on_result=on_filepicker_input)
    directorypicker = ft.FilePicker(on_result=on_filepicker_output)
    page.overlay.extend([filepicker, directorypicker])
    page.update()

    input_file_name = ""
    input_path = ft.Text("Select a file to compress", size=22, no_wrap=True, color='#f0f0f0')
    output_directory = ft.Text("Select a output directory", size=22, no_wrap=True, color='#f0f0f0')

    page.add(
        ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Text("Abyss compressor", size=34, weight=ft.FontWeight.W_900)
                ),

                # Header divider
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Divider(thickness=2),
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Text("Operations", size=26, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.symmetric(horizontal=5)
                        ),
                        ft.Container(
                            content=ft.Divider(thickness=2),
                            expand=True
                        )
                    ],
                    expand=True
                ),

                # File to compress input
                ft.Row(
                    controls=[
                        ft.Container(
                            content=input_path,
                            width=310,
                            height=40,
                            bgcolor='#1c1c1c',
                            alignment=ft.alignment.center_left,
                            border_radius=10,
                            padding=ft.padding.only(left=5)
                        ),
                        ft.ElevatedButton(
                            "select", 
                            style=ft.ButtonStyle(text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)), 
                            on_click=lambda _: filepicker.pick_files("Select a files"), 
                            width=120, 
                            height=40,
                            color="#f0f0f0",
                            bgcolor='#1c1c1c'
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CANCEL,
                            on_click=lambda _: on_input_close(),
                            icon_color=ft.Colors.RED,
                            scale=1.5
                        )
                    ]
                ),

                # Output directory input
                ft.Row(
                    controls=[
                        ft.Container(
                            content=output_directory,
                            width=310,
                            height=40,
                            bgcolor='#1c1c1c',
                            alignment=ft.alignment.center_left,
                            border_radius=10,
                            padding=ft.padding.only(left=5)
                        ),
                        ft.ElevatedButton(
                            "select", 
                            style=ft.ButtonStyle(text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)), 
                            on_click=lambda _: directorypicker.get_directory_path("Select a directory"), 
                            width=120, 
                            height=40,
                            color='#f0f0f0',
                            bgcolor='#1c1c1c'
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CANCEL,
                            on_click=lambda _: on_output_close(),
                            icon_color=ft.Colors.RED,
                            scale=1.5
                        )
                    ]
                ),

                # Operations buttons
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                                "compress", 
                                style=ft.ButtonStyle(text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)), 
                                on_click=lambda _: on_compress_click(input_path.value, f"{output_directory.value}/{input_file_name}"), 
                                width=235, 
                                height=50,
                                color="#f0f0f0",
                                bgcolor='#1c1c1c'
                        ),
                        ft.ElevatedButton(
                                "decompress", 
                                style=ft.ButtonStyle(text_style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)), 
                                on_click=lambda _: on_decompress_click(input_path.value, f"{output_directory.value}/{input_file_name}"), 
                                width=235, 
                                height=50,
                                color="#f0f0f0",
                                bgcolor='#1c1c1c'
                        )
                    ]
                ),

                # Upper options divider
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Divider(thickness=2),
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Text("Options", size=26, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.symmetric(horizontal=5)
                        ),
                        ft.Container(
                            content=ft.Divider(thickness=2),
                            expand=True
                        )
                    ],
                    expand=True
                ),
                # Settings
                ft.Column(
                    controls=[
                        ft.Text("In development", size=22)
                    ]
                )
            ],
            spacing=20
        )
        
    )

ft.app(target=main)
