import random
import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "TheEthicalVideo"
    
    page.spacing = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_pause(e):
        video.pause()
        print("Video.pause()")

    def handle_play_or_pause(e):
        video.play_or_pause()
        print("Video.play_or_pause()")

    def handle_play(e):
        video.play()
        print("Video.play()")

    def handle_stop(e):
        video.stop()
        print("Video.stop()")

    def handle_next(e):
        video.next()
        print("Video.next()")

    def handle_previous(e):
        video.previous()
        print("Video.previous()")

    def handle_volume_change(e):
        video.volume = e.control.value
        page.update()
        print(f"Video.volume = {e.control.value}")

    def handle_playback_rate_change(e):
        video.playback_rate = e.control.value
        page.update()
        print(f"Video.playback_rate = {e.control.value}")

    def handle_seek(e):
        video.seek(10000)
        print(f"Video.seek(10000)")

    def handle_add_media(e):
        video.playlist_add(random.choice(sample_media))
        print(f"Video.playlist_add(random.choice(sample_media))")

    def handle_remove_media(e):
        r = random.randint(0, len(video.playlist) - 1)
        video.playlist_remove(r)
        print(f"Popped Item at index: {r} (position {r+1})")

    def handle_jump(e):
        print(f"Video.jump_to(0)")
        video.jump_to(0)

    sample_media = [
        ft.VideoMedia(
            "https://www.youtube.com/watch?v=KSD7_QPwYt8"
        ),
        ft.VideoMedia(
            "https://www.youtube.com/watch?v=KSD7_QPwYt8"
        ),
        ft.VideoMedia(
            "https://www.youtube.com/watch?v=KSD7_QPwYt8"
        ),
        ft.VideoMedia(
            "https://www.youtube.com/watch?v=KSD7_QPwYt8"
        ),
        ft.VideoMedia(
            "https://www.youtube.com/watch?v=KSD7_QPwYt8",
            extras={
                "artist": "Thousand Foot Krutch",
                "album": "The End Is Where We Begin",
            },
            http_headers={
                "Foo": "Bar",
                "Accept": "*/*",
            },
        ),
    ]

    page.add(
        video := ft.Video(
            expand=True,
            playlist=sample_media[0:2],
            playlist_mode=ft.PlaylistMode.LOOP,
            fill_color=ft.colors.BLUE_400,
            aspect_ratio=16/9,
            volume=100,
            autoplay=False,
            filter_quality=ft.FilterQuality.HIGH,
            muted=False,
            on_loaded=lambda e: print("Video loaded successfully!"),
            on_enter_fullscreen=lambda e: print("Video entered fullscreen!"),
            on_exit_fullscreen=lambda e: print("Video exited fullscreen!"),
        ),
        ft.Row(
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ElevatedButton("Play", on_click=handle_play),
                ft.ElevatedButton("Pause", on_click=handle_pause),
                ft.ElevatedButton("Play Or Pause", on_click=handle_play_or_pause),
                ft.ElevatedButton("Stop", on_click=handle_stop),
                ft.ElevatedButton("Next", on_click=handle_next),
                ft.ElevatedButton("Previous", on_click=handle_previous),
                ft.ElevatedButton("Seek s=10", on_click=handle_seek),
                ft.ElevatedButton("Jump to first Media", on_click=handle_jump),
                ft.ElevatedButton("Add Random Media", on_click=handle_add_media),
                ft.ElevatedButton("Remove Random Media", on_click=handle_remove_media),
            ],
        ),
        ft.Slider(
            min=0,
            value=100,
            max=100,
            label="Volume = {value}%",
            divisions=10,
            width=400,
            on_change=handle_volume_change,
        ),
        ft.Slider(
            min=1,
            value=1,
            max=3,
            label="PlaybackRate = {value}X",
            divisions=6,
            width=400,
            on_change=handle_playback_rate_change,
        ),
    )


ft.app(target=main)