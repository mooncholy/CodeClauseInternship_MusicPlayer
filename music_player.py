"""
Basic Features:
1. Playback controls
    Play, Pause, Stop, Next, Previous, Rewind
2. Song Information Display
    Song Title, Artist, Album, Duration
"""
# In terminal: pip install pygame

# Importing Required Libraries
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pygame import mixer
import sv_ttk

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('Task 2: Music Player')
        self.root.resizable(False, False)
        self.root.geometry("552x770")

        # Initialization
        mixer.init()
        self.song_list = []
        self.current_song_index = 0

        # Create GUI
        self.create_widgets()

    # Create GUI organization
    def create_widgets(self):
        # Album art
        self.album_image = tk.PhotoImage(file='./imgs/music.png')
        self.album_label = ttk.Label(self.root, image=self.album_image)
        self.album_label.grid(column=0, row=0, columnspan=3, pady=10, padx=10)

        # Song Information
        self.song_title_label = ttk.Label(self.root, text="Song Title", font=('Courier', 12), wraplength=500, justify="center")
        self.song_title_label.grid(column=0, row=1, columnspan=3)
        self.artist_label = ttk.Label(self.root, text="Artist", font=('Courier', 10))
        self.artist_label.grid(column=0, row=2, columnspan=3)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(self.root, variable=self.progress_var, orient="horizontal", length=440)
        self.progress_bar.grid(column=0, row=3, columnspan=3, pady=10, padx=20, sticky='we')

        # Rewind button
        self.rewind_icon = tk.PhotoImage(file="./imgs/rewind.png", width=50, height=50)
        self.rewind_button = ttk.Button(self.root, image=self.rewind_icon, command=self.rewind_music)
        self.rewind_button.grid(column=2, row=2, padx=10, sticky='e')

        # Play/Pause button
        self.play_pause_btn = ttk.Button(self.root, text="Play", command=self.play_pause_music)
        self.play_pause_btn.grid(column=1, row=4, pady=10, sticky='ew')

        # Next and Previous buttons
        self.previous_btn = ttk.Button(self.root, text="Previous", command=self.play_previous)
        self.previous_btn.grid(column=0, row=4, padx=10, sticky='ew')
        self.next_btn = ttk.Button(self.root, text="Next", command=self.play_next)
        self.next_btn.grid(column=2, row=4, padx=10, sticky='ew')

        # Browse songs button
        self.browse_btn = ttk.Button(self.root, text="Add Songs", command=self.add_music)
        self.browse_btn.grid(column=0, row=5, columnspan=3, pady=5,padx=18,  sticky='ew')

        # Apply Theme
        sv_ttk.use_light_theme()

    # Player Functionalities
    def add_music(self):
        files = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
        for file in files:
            self.song_list.append(file)
        self.update_song_info()
        self.load_and_play()

    # Update album art and song information
    def update_song_info(self):
        if self.song_list:
            current_song = self.song_list[self.current_song_index]
            self.song_title_label.configure(text=current_song.split('/')[-1])
            self.artist_label.configure(text="Unknown Artist")

    # Play song
    def play_pause_music(self):
        if mixer.music.get_busy():
            mixer.music.pause()
            self.play_pause_btn.configure(text="Play")
        else:
            if self.song_list:
                mixer.music.unpause()
                self.play_pause_btn.configure(text="Pause")
            else:
                self.song_title_label.configure(text="No Song in Queue. Press Add songs to add a file to play")
                self.artist_label.configure(text="")

    # Play next and previous songs
    def play_next(self):
        if self.song_list:
            self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
            self.load_and_play()

    def play_previous(self):
        if self.song_list:
            self.current_song_index = (self.current_song_index - 1) % len(self.song_list)
            self.load_and_play()

    def load_and_play(self):
        if self.song_list:
            mixer.music.load(self.song_list[self.current_song_index])
            mixer.music.play()
            self.play_pause_btn.configure(text="Pause")
            self.update_song_info()
            #self.update_progress_bar()

    # Rewind 15 sec
    def rewind_music(self):
        if mixer.music.get_busy():
            current_pos = mixer.music.get_pos() / 1000.0
            new_pos = max(0, int(current_pos - 15))
            mixer.music.play(start=new_pos)

    # Show progress bar
    def update_progress_bar(self):
        if mixer.music.get_busy():
            song_length = mixer.Sound(self.song_list[self.current_song_index]).get_length()
            current_pos = mixer.music.get_pos() / 1000.0
            self.progress_var.set(current_pos / song_length)
        self.root.after(1000, self.update_progress_bar)


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()