import tkinter as tk
from menu import GUIWithMenu


def main():
    root = tk.Tk()
    app = GUIWithMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
