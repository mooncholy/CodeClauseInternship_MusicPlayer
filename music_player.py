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
import threading
import mutagen, eyed3
from mutagen.mp3 import MP3
import os, glob, re, cv2

class MusicPlayer:
    def __init__(self, root, notebook):
        self.root = root
        self.notebook = notebook

        # Initialization
        mixer.init()
        self.song_list = []
        self.current_song_index = 0

        # Create GUI
        self.create_widgets()

        # Starting Daemon Thread
        self.worker()

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
        self.progress_var = self.song_length = tk.DoubleVar()
        self.progress_bar = ttk.Scale(self.root, variable=self.progress_var, orient="horizontal", length=440)
        self.progress_bar.grid(column=0, row=3, columnspan=3, pady=10, padx=20, sticky='we')

        # Rewind button
        #self.rewind_icon = tk.PhotoImage(file="./imgs/rewind.png", width=50, height=50)
        #self.rewind_button = ttk.Button(self.root, image=self.rewind_icon, command=self.rewind_music)
        #self.rewind_button.grid(column=2, row=2, padx=10, sticky='e')

        # Play/Pause button
        self.play_pause_btn = ttk.Button(self.root, text="Play", command=self.play_pause_music)
        self.play_pause_btn.grid(column=1, row=4, pady=10, sticky='ew')

        # Next and Previous buttons
        self.previous_btn = ttk.Button(self.root, text="Previous", command=self.play_previous)
        self.previous_btn.grid(column=0, row=4, padx=10, sticky='ew')
        self.next_btn = ttk.Button(self.root, text="Next", command=self.play_next)
        self.next_btn.grid(column=2, row=4, padx=10, sticky='ew')

        # Browse songs button
        self.browse_btn = ttk.Button(self.root, text="Add Songs", command=self.select_folder)
        self.browse_btn.grid(column=0, row=5, columnspan=3, pady=5,padx=18,  sticky='ew')

        # Apply Theme
        sv_ttk.use_light_theme()

    # Player Functionalities

    # Add music to queue
    def add_music(self):
        files = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
        for file in files:
            self.song_list.append(file)
        #self.create_playlist_queue()
        self.update_song_info()
        self.load_and_play()

    # Create Playlist Queue
    #def create_playlist_queue(self):

    # Open all songs in a directoru
    def select_folder(self):
        music_dir = filedialog.askdirectory()
        if music_dir:
            self.song_list = []
            for filename in glob.glob(os.path.join(music_dir, "*.mp3")):
                current_path = re.sub(r"\\", "/", os.path.normpath(filename))
                self.song_list.append(current_path)
            print(f"{self.song_list}\n{self.current_song_index}\n{self.song_list[self.current_song_index]}")
            self.update_song_info()
            self.load_and_play()


    # Update album art and song information
    def update_song_info(self):
        if self.song_list:
            current_song = os.path.basename(self.song_list[self.current_song_index])
            self.song_title_label.configure(text=current_song.split('/')[-1])
            meta = mutagen.File(self.song_list[self.current_song_index], easy=True)
            if meta:
                if meta['artist'][0]:
                    self.artist_label.configure(text=meta['artist'][0])
                elif meta['albumartist'][0]:
                    self.artist_label.configure(text=meta['albumartist'][0])
                else:
                    self.artist_label.configure(text="Unknown Artist")
            else:
                self.artist_label.configure(text="Unknown Artist")
            self.update_album_art()

    # Replace Album Art
    def update_album_art(self):
        if os.path.exists('./imgs/album_art.png'):
            os.remove('./imgs/album_art.png')
            self.album_label.configure(image=self.album_image)
        audio_file = eyed3.load(self.song_list[self.current_song_index])
        for image in audio_file.tag.images:
            image_file = open("./imgs/album_art.png", "wb")
            print(image)
            image_file.write(image.image_data)
            image_file = cv2.imread("./imgs/album_art.png")
            try:
                image_file = cv2.resize(image_file, (512,512))
                cv2.imwrite("./imgs/album_art.png", image_file)
                image_tk = tk.PhotoImage(file="./imgs/album_art.png")
                self.album_label.configure(image=image_tk)
                self.album_label.image = image_tk
            except:
                self.album_label.configure(image=self.album_image)

    # Play song
    def play_pause_music(self):
        if mixer.music.get_busy():
            mixer.music.pause()
            self.play_pause_btn.configure(text="Play")
        else:
            if self.song_list:
                mixer.music.pause()
                mixer.music.unpause()
                self.play_pause_btn.configure(text="Pause")
            else:
                self.song_title_label.configure(text="No Song in Queue. Press Add songs to add a file to play")
                self.artist_label.configure(text="")
            self.worker()

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
            self.worker()

    # Rewind 15 sec
    def rewind_music(self):
        if mixer.music.get_busy():
            current_pos = mixer.music.get_pos() / 1000.0
            new_pos = max(0, int(current_pos - 15))
            mixer.music.play(start=new_pos)

    # Show progress bar
    def update_progress_bar(self):
        if mixer.music.get_busy():
            self.song_length = MP3(self.song_list[self.current_song_index]).info.length
            current_pos = mixer.music.get_pos() / 1000.0
            self.progress_var.set(current_pos / self.song_length)
            #print(self.progress_var.get())
            self.root.after(1000, self.update_progress_bar)

    # Running background function in a daemon thread
    def worker(self):
        t = threading.Thread(target=self.update_progress_bar, daemon=True)
        t.start()


if __name__ == "__main__":
    # Main Player Window
    root = tk.Tk()
    root.title('Task 2: Music Player')
    root.resizable(False, False)
    root.minsize(552, 770)

    # Music Player interface Tab
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    music_frame = tk.Frame(notebook)
    music_player = MusicPlayer(music_frame, notebook)
    notebook.add(music_frame, text="Music Player")

    # Playlist Queue Interface Tab
    playlist_queue_frame = tk.Frame(notebook)
    notebook.add(playlist_queue_frame, text="Playlist Queue")
    root.mainloop()

