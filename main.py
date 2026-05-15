# ================================
# 🎬 ADVANCED MOVIE RECOMMENDATION SYSTEM
# ================================

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import random

FILE = "soham.txt"

GENRES = [
    "All", "Action", "Comedy", "Drama", "Horror",
    "Sci-Fi", "Romance", "Thriller", "Crime",
    "Adventure", "Fantasy", "Animation", "Biography"
]

OTTS = [
    "All", "Netflix", "Amazon Prime Video",
    "Disney+ Hotstar", "JioCinema",
    "SonyLIV", "Zee5", "Apple TV+"
]


# ================================
# LOAD MOVIES
# ================================

def load_movies():

    movies = []

    if not os.path.exists(FILE):
        return movies

    with open(FILE, "r", encoding="utf-8") as f:

        for line in f:

            parts = line.strip().split(",")

            if len(parts) >= 4:

                try:

                    movies.append({
                        "name": parts[0],
                        "genre": parts[1],
                        "rating": float(parts[2]),
                        "ott": parts[3]
                    })

                except:
                    pass

    return movies


# ================================
# MAIN APP
# ================================

class App:

    def __init__(self, root):

        self.root = root

        self.root.title("🎬 CineScope India Pro")

        self.root.geometry("1450x820")

        self.root.config(bg="#d8f3dc")

        self.movies = load_movies()

        self.build_ui()

    # ================================
    # UI
    # ================================

    def build_ui(self):

        # HEADER
        header = tk.Frame(
            self.root,
            bg="#95d5b2",
            height=70
        )

        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="🎬 CineScope India Pro",
            font=("Arial", 24, "bold"),
            bg="#95d5b2",
            fg="#1b4332"
        ).pack(side=tk.LEFT, padx=20)

        self.stats_var = tk.StringVar()

        tk.Label(
            header,
            textvariable=self.stats_var,
            font=("Arial", 11, "bold"),
            bg="#95d5b2",
            fg="#081c15"
        ).pack(side=tk.RIGHT, padx=20)

        self.refresh_stats()

        # BODY
        body = tk.Frame(self.root, bg="#d8f3dc")

        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # LEFT PANEL
        left = tk.Frame(
            body,
            bg="#b7e4c7",
            width=320
        )

        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        left.pack_propagate(False)

        tk.Label(
            left,
            text="⚙ CONTROL PANEL",
            font=("Arial", 16, "bold"),
            bg="#b7e4c7",
            fg="#1b4332"
        ).pack(pady=15)

        # SEARCH
        tk.Label(
            left,
            text="Search Movie",
            bg="#b7e4c7",
            fg="black",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=10)

        self.search_var = tk.StringVar()

        tk.Entry(
            left,
            textvariable=self.search_var,
            font=("Arial", 11),
            bg="#edf6f9"
        ).pack(fill=tk.X, padx=10, pady=5)

        # GENRE
        tk.Label(
            left,
            text="Genre",
            bg="#b7e4c7",
            fg="black",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=10)

        self.genre_var = tk.StringVar(value="All")

        ttk.Combobox(
            left,
            textvariable=self.genre_var,
            values=GENRES,
            state="readonly"
        ).pack(fill=tk.X, padx=10, pady=5)

        # OTT
        tk.Label(
            left,
            text="OTT Platform",
            bg="#b7e4c7",
            fg="black",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=10)

        self.ott_var = tk.StringVar(value="All")

        ttk.Combobox(
            left,
            textvariable=self.ott_var,
            values=OTTS,
            state="readonly"
        ).pack(fill=tk.X, padx=10, pady=5)

        # BUTTONS
        buttons = [

            ("📋 Browse Movies", self.view_movies, "#40916c"),

            ("🔍 Search", self.search_movies, "#52b788"),

            ("💡 Recommend", self.recommend_movies, "#2d6a4f"),

            ("🏆 Top Rated", self.show_top_movies, "#1b4332"),

            ("📡 OTT Analysis", self.show_ott_analysis, "#40916c"),

            ("📊 Dashboard", self.show_dashboard, "#52b788"),

            ("🔥 Trending", self.show_trending, "#2d6a4f")

        ]

        for text, command, color in buttons:

            tk.Button(
                left,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 11, "bold"),
                relief=tk.FLAT,
                cursor="hand2"
            ).pack(fill=tk.X, padx=10, pady=5, ipady=7)

        # RIGHT PANEL
        right = tk.Frame(
            body,
            bg="#b7e4c7"
        )

        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.title_lbl = tk.Label(
            right,
            text="📊 ANALYTICS DASHBOARD",
            font=("Arial", 18, "bold"),
            bg="#b7e4c7",
            fg="#1b4332"
        )

        self.title_lbl.pack(pady=10)

        self.canvas_frame = tk.Frame(
            right,
            bg="#b7e4c7"
        )

        self.canvas_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.show_dashboard()

    # ================================
    # STATS
    # ================================

    def refresh_stats(self):

        total = len(self.movies)

        avg = (
            sum(m["rating"] for m in self.movies) / total
            if total else 0
        )

        self.stats_var.set(
            f"🎬 Movies: {total}   ⭐ Avg Rating: {avg:.1f}"
        )

    # ================================
    # FILTER
    # ================================

    def filtered(self):

        genre = self.genre_var.get()

        ott = self.ott_var.get()

        query = self.search_var.get().lower()

        return [

            m for m in self.movies

            if
            (genre == "All" or genre.lower() in m["genre"].lower())

            and

            (ott == "All" or ott.lower() in m["ott"].lower())

            and

            (query in m["name"].lower())

        ]

    # ================================
    # CLEAR
    # ================================

    def clear(self):

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

    # ================================
    # DRAW GRAPH
    # ================================

    def draw_chart(self, fig):

        self.clear()

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.canvas_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

    # ================================
    # TABLE
    # ================================

    def show_table(self, data, title):

        self.clear()

        self.title_lbl.config(text=title)

        tree = ttk.Treeview(
            self.canvas_frame,
            columns=("Movie", "Genre", "Rating", "OTT"),
            show="headings"
        )

        cols = ["Movie", "Genre", "Rating", "OTT"]

        widths = [350, 180, 100, 220]

        for col, width in zip(cols, widths):

            tree.heading(col, text=col)

            tree.column(col, width=width)

        for m in data:

            tree.insert(
                "",
                tk.END,
                values=(
                    m["name"],
                    m["genre"],
                    m["rating"],
                    m["ott"]
                )
            )

        tree.pack(fill=tk.BOTH, expand=True)

    # ================================
    # VIEW
    # ================================

    def view_movies(self):

        self.show_table(
            self.movies,
            "📋 ALL MOVIES"
        )

    # ================================
    # SEARCH
    # ================================

    def search_movies(self):

        self.show_table(
            self.filtered(),
            "🔍 SEARCH RESULTS"
        )

    # ================================
    # RECOMMEND
    # ================================

    def recommend_movies(self):

        self.title_lbl.config(
            text="💡 SMART RECOMMENDATIONS"
        )

        data = sorted(
            self.filtered(),
            key=lambda x: x["rating"],
            reverse=True
        )[:10]

        names = [m["name"][:18] for m in data]

        ratings = [m["rating"] for m in data]

        fig = Figure(
            figsize=(10, 6),
            facecolor="#d8f3dc"
        )

        ax = fig.add_subplot(111)

        ax.set_facecolor("#edf6f9")

        colors = plt.cm.viridis(
            [i / len(names) for i in range(len(names))]
        )

        bars = ax.barh(
            names,
            ratings,
            color=colors,
            edgecolor="black"
        )

        for bar, value in zip(bars, ratings):

            ax.text(
                value + 0.1,
                bar.get_y() + bar.get_height()/2,
                str(value),
                va='center',
                fontsize=10,
                fontweight='bold'
            )

        ax.set_title(
            "🎯 AI Recommended Movies",
            fontsize=20,
            fontweight="bold",
            color="#1b4332"
        )

        ax.grid(
            axis='x',
            linestyle='--',
            alpha=0.4
        )

        fig.tight_layout()

        self.draw_chart(fig)

    # ================================
    # TOP MOVIES
    # ================================

    def show_top_movies(self):

        self.title_lbl.config(
            text="🏆 TOP RATED MOVIES"
        )

        data = sorted(
            self.movies,
            key=lambda x: x["rating"],
            reverse=True
        )[:10]

        names = [m["name"][:15] for m in data]

        ratings = [m["rating"] for m in data]

        fig = Figure(
            figsize=(10, 6),
            facecolor="#d8f3dc"
        )

        ax = fig.add_subplot(111)

        ax.set_facecolor("#edf6f9")

        colors = plt.cm.plasma(
            [i / len(names) for i in range(len(names))]
        )

        bars = ax.bar(
            names,
            ratings,
            color=colors,
            edgecolor="black",
            linewidth=1.2
        )

        for bar, val in zip(bars, ratings):

            ax.text(
                bar.get_x() + bar.get_width()/2,
                val + 0.1,
                str(val),
                ha='center',
                fontsize=10,
                fontweight='bold'
            )

        ax.set_title(
            "⭐ Highest Rated Movies",
            fontsize=20,
            fontweight="bold",
            color="#1b4332"
        )

        ax.grid(
            axis='y',
            linestyle='--',
            alpha=0.4
        )

        plt.setp(
            ax.get_xticklabels(),
            rotation=20
        )

        fig.tight_layout()

        self.draw_chart(fig)

    # ================================
    # OTT ANALYSIS
    # ================================

    def show_ott_analysis(self):

        self.title_lbl.config(
            text="📡 OTT PLATFORM ANALYSIS"
        )

        ott_count = {}

        for m in self.movies:

            ott_count[m["ott"]] = ott_count.get(m["ott"], 0) + 1

        fig = Figure(
            figsize=(10, 6),
            facecolor="#d8f3dc"
        )

        ax = fig.add_subplot(111)

        colors = plt.cm.Set3(
            range(len(ott_count))
        )

        explode = [0.04] * len(ott_count)

        ax.pie(
            ott_count.values(),
            labels=ott_count.keys(),
            autopct='%1.1f%%',
            colors=colors,
            explode=explode,
            shadow=True,
            startangle=90
        )

        ax.set_title(
            "🎬 Movies on OTT Platforms",
            fontsize=20,
            fontweight="bold",
            color="#1b4332"
        )

        fig.tight_layout()

        self.draw_chart(fig)

    # ================================
    # DASHBOARD
    # ================================

    def show_dashboard(self):

        self.title_lbl.config(
            text="📊 ADVANCED DASHBOARD"
        )

        genre_count = {}

        for m in self.movies:

            genre = m["genre"]

            genre_count[genre] = (
                genre_count.get(genre, 0) + 1
            )

        genres = list(genre_count.keys())

        counts = list(genre_count.values())

        fig = Figure(
            figsize=(11, 6),
            facecolor="#d8f3dc"
        )

        ax = fig.add_subplot(111)

        ax.set_facecolor("#edf6f9")

        colors = plt.cm.rainbow(
            [i / len(genres) for i in range(len(genres))]
        )

        bars = ax.bar(
            genres,
            counts,
            color=colors,
            edgecolor="#1b4332",
            linewidth=1.5
        )

        # GLOW EFFECT
        for bar in bars:

            bar.set_alpha(0.9)

        # VALUES
        for bar in bars:

            height = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width()/2,
                height + 1,
                str(height),
                ha='center',
                fontsize=10,
                fontweight='bold',
                color="#1b4332"
            )

        ax.set_title(
            "🎭 Genre Distribution Analytics",
            fontsize=22,
            fontweight="bold",
            color="#1b4332",
            pad=20
        )

        ax.grid(
            axis='y',
            linestyle='--',
            alpha=0.3
        )

        ax.tick_params(
            axis='x',
            rotation=20,
            labelsize=10
        )

        ax.spines['top'].set_visible(False)

        ax.spines['right'].set_visible(False)

        fig.tight_layout()

        self.draw_chart(fig)

    # ================================
    # TRENDING
    # ================================

    def show_trending(self):

        self.title_lbl.config(
            text="🔥 TRENDING MOVIES"
        )

        data = random.sample(
            self.movies,
            min(10, len(self.movies))
        )

        self.show_table(
            data,
            "🔥 TRENDING MOVIES"
        )


# ================================
# RUN
# ================================

if __name__ == "__main__":

    root = tk.Tk()

    app = App(root)

    root.mainloop()