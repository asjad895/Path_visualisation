
import tkinter as tk
import queue
import time
from tkinter import PhotoImage
def create_colored_icon(color, size=20):
    icon = tk.PhotoImage(width=size, height=size)
    icon.put(color, to=(0, 0, size, size))
    return icon
GRID_WIDTH = 30
GRID_HEIGHT = 30
# Initialize the grid with zeros (0 represents an empty cell)
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Constants for colors
EMPTY_COLOR = "white"
OBSTACLE_COLOR = "black"
VISITED_COLOR = "pink"
PATH_COLOR = "yellow"

# Define directions (up, down, left, right)
directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Variables to store the user-selected start and end points
start_point = None
end_point = None

def draw_grid(canvas):
    cell_width = canvas.winfo_width() // GRID_WIDTH
    cell_height = canvas.winfo_height() // GRID_HEIGHT
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            x1, y1 = col * cell_width, row * cell_height
            x2, y2 = x1 + cell_width, y1 + cell_height
            color = EMPTY_COLOR if grid[row][col] == 0 else OBSTACLE_COLOR
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="SkyBlue1")

def set_start_point(event):
    global start_point
    row = event.y // (canvas.winfo_height() // GRID_HEIGHT)
    col = event.x // (canvas.winfo_width() // GRID_WIDTH)
    if grid[row][col] != 1:  # Check that the clicked cell is not an obstacle
        # Clear previous start point (if any)
        if start_point:
            prev_row, prev_col = start_point
            grid[prev_row][prev_col] = 0
            canvas.create_rectangle(prev_col * (canvas.winfo_width() // GRID_WIDTH), prev_row * (canvas.winfo_height() // GRID_HEIGHT),
                                    (prev_col + 1) * (canvas.winfo_width() // GRID_WIDTH), (prev_row + 1) * (canvas.winfo_height() // GRID_HEIGHT),
                                    fill=EMPTY_COLOR)
        start_point = (row, col)
        canvas.create_rectangle(col * (canvas.winfo_width() // GRID_WIDTH), row * (canvas.winfo_height() // GRID_HEIGHT),
                                (col + 1) * (canvas.winfo_width() // GRID_WIDTH), (row + 1) * (canvas.winfo_height() // GRID_HEIGHT),
                                fill="green")
        clear_path()  # Clear the path when the start point changes

def set_end_point(event):
    global end_point
    row = event.y // (canvas.winfo_height() // GRID_HEIGHT)
    col = event.x // (canvas.winfo_width() // GRID_WIDTH)
    if grid[row][col] != 1:  # Check that the clicked cell is not an obstacle
        # Clear previous end point (if any)
        if end_point:
            prev_row, prev_col = end_point
            grid[prev_row][prev_col] = 0
            canvas.create_rectangle(prev_col * (canvas.winfo_width() // GRID_WIDTH), prev_row * (canvas.winfo_height() // GRID_HEIGHT),
                                    (prev_col + 1) * (canvas.winfo_width() // GRID_WIDTH), (prev_row + 1) * (canvas.winfo_height() // GRID_HEIGHT),
                                    fill=EMPTY_COLOR)
        end_point = (row, col)
        canvas.create_rectangle(col * (canvas.winfo_width() // GRID_WIDTH), row * (canvas.winfo_height() // GRID_HEIGHT),
                                (col + 1) * (canvas.winfo_width() // GRID_WIDTH), (row + 1) * (canvas.winfo_height() // GRID_HEIGHT),
                                fill="red")
        clear_path()  # Clear the path when the end point changes

def clear_path():
    # Clear the path
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col] == 2:
                grid[row][col] = 0
                canvas.create_rectangle(col * (canvas.winfo_width() // GRID_WIDTH), row * (canvas.winfo_height() // GRID_HEIGHT),
                                        (col + 1) * (canvas.winfo_width() // GRID_WIDTH), (row + 1) * (canvas.winfo_height() // GRID_HEIGHT),
                                        fill=EMPTY_COLOR)


def toggle_obstacle(event):
    row = event.y // (canvas.winfo_height() // GRID_HEIGHT)
    col = event.x // (canvas.winfo_width() // GRID_WIDTH)
    if (row, col) != start_point and (row, col) != end_point:  # Don't change start or end points
        grid[row][col] = 1 if grid[row][col] == 0 else 0  # Toggle obstacle status
        color = OBSTACLE_COLOR if grid[row][col] == 1 else EMPTY_COLOR
        canvas.create_rectangle(col * (canvas.winfo_width() // GRID_WIDTH), row * (canvas.winfo_height() // GRID_HEIGHT),
                                (col + 1) * (canvas.winfo_width() // GRID_WIDTH), (row + 1) * (canvas.winfo_height() // GRID_HEIGHT),
                                fill=color)

def clear_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            grid[row][col] = 0
    canvas.delete("all")
    draw_grid(canvas)

global t
def color_path(end_row,end_col,cell_width,cell_height,path):
    
    row, col = end_row, end_col
    while row != -1 and col != -1:
        if (row, col) != start_point and (row, col) != end_point:
            # Color the path yellow (excluding start and end points)
            canvas.create_rectangle(col * cell_width, row * cell_height,
                                    (col + 1) * cell_width, (row + 1) * cell_height,
                                    fill="yellow")
        grid[row][col] = 2  # Marking the path
        row, col = path[row][col]

    canvas.update()
def update_visualization(q,end_row,end_col,visited,visited_nodes,path,cell_width,cell_height,start_time):
    if not q.empty():
        row, col = q.get()
        visited_nodes += 1
        if row == end_row and col == end_col:
            print("PAAHUNCG GAY  ")
            # color_path(end_row,end_col,cell_width,cell_height,path)
            # Calculate the time taken
            end_time = time.time()
            time_taken = end_time - start_time
            t = time_taken
            # Print information in the UI
            info_label.config(text=f"Total Visited Nodes: {visited_nodes}\nTime Taken: {t:.4f} seconds")
            return

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH and not visited[new_row][new_col] and grid[new_row][new_col] == 0:
                visited[new_row][new_col] = True
                path[new_row][new_col] = (row, col)
                print("path:", row, col)
                q.put((new_row, new_col))

                # Visualization: Color visited cells pink (except start and end points)
                if (new_row, new_col) != start_point and (new_row, new_col) != end_point:
                    canvas.create_rectangle(new_col * cell_width, new_row * cell_height,
                                            (new_col + 1) * cell_width, (new_row + 1) * cell_height,
                                            fill="pink")

                canvas.update()  # Update the canvas
        root.after(10, update_visualization(q,end_row,end_col,visited,visited_nodes,path,cell_width,cell_height,start_time)) 

def start_pathfinding():
    global start_point, end_point
    if start_point and end_point:
        start_time = time.time()  # Record the start time
        start_row, start_col = start_point
        end_row, end_col = end_point
        print("End:",end_row,end_col)
        visited = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        path = [[(-1, -1) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        # Calculate cell width and height
        cell_width = canvas.winfo_width() // GRID_WIDTH
        cell_height = canvas.winfo_height() // GRID_HEIGHT
        # Use a queue for BFS
        q = queue.Queue()
        q.put((start_row, start_col))
        print("LKHKHUKUGUD")
        visited_nodes = 0
        update_visualization(q,end_row,end_col,visited,visited_nodes,path,cell_width,cell_height,start_time)
        print("FHHYF^&(*)")


root = tk.Tk()
root.configure(bg='snow')
root.title("Pathfinding Visualization")

# Create a navigation bar (frame) at the top
nav_bar = tk.Frame(root,height=100)
nav_bar.pack(side=tk.TOP,fill='both',pady=(0, 10))

# Create "Start" and "Clear" buttons in the navigation bar
start_button = tk.Button(nav_bar, text="Start Pathfinding",background='Steel Blue1',font=("Arial", 12),command=start_pathfinding)
start_button.pack(side=tk.LEFT, padx=10)

# Create icons
red_icon = create_colored_icon("red")
green_icon = create_colored_icon("green")
black_icon = create_colored_icon("black")

# Create and place labels with icons
goal_label = tk.Label(nav_bar, image=red_icon, text="Goal Node",compound="left",background='Steel Blue1', font=("Arial", 12))
goal_label.pack(side=tk.LEFT,padx=10)
start_label = tk.Label(nav_bar, image=green_icon, text="Start Node",compound="left",background='Steel Blue1', font=("Arial", 12))
start_label.pack(side=tk.LEFT,padx=10)
wall_label = tk.Label(nav_bar, image=black_icon, text="Wall",compound="left",background='Steel Blue1', font=("Arial", 12))
wall_label.pack(side=tk.LEFT,padx=10)

clear_button = tk.Button(nav_bar, text="Clear Grid", background='Steel Blue1',font=("Arial", 12),command=clear_grid)
clear_button.pack(side=tk.LEFT, padx=10)
nav_bar.configure(bg="medium blue")
info_label = tk.Label(root, text="", font=("Arial", 12),background='ghost white',fg='navy')
info_label.pack(side=tk.RIGHT, padx=10)

cell_width = 30  # Increase this value to make cells wider
cell_height = 30  # Increase this value to make cells taller
# Update the canvas size based on the new cell dimensions
canvas = tk.Canvas(root, width=GRID_WIDTH * cell_width, height=GRID_HEIGHT * cell_height)
canvas.pack(expand=True)

# Draw the initial grid
draw_grid(canvas)
# Define a function to handle algorithm selection
def algorithm_selected(algorithm):
    print(f"Selected Algorithm: {algorithm}")


# Define a list of search algorithms
search_algorithms = ["Algorithm 1", "Algorithm 2", "Algorithm 3", "Algorithm 4"]

# Create a Tkinter StringVar to store the selected algorithm
selected_algorithm = tk.StringVar()
selected_algorithm.set(search_algorithms[0])  # Set the default algorithm

# Create an OptionMenu widget for selecting the algorithm
algorithm_menu = tk.OptionMenu(nav_bar, selected_algorithm, *search_algorithms)
algorithm_menu.pack(padx=20, pady=20)

# Create a button to trigger the selection
select_button = tk.Button(root, text="Select", command=lambda: algorithm_selected(selected_algorithm.get()))
select_button.pack()
# Bind events to set start and end points and toggle obstacles
canvas.bind("<Button-1>", set_start_point)
canvas.bind("<Button-3>", set_end_point)
canvas.bind("<B1-Motion>", toggle_obstacle)

# Main loop
root.mainloop()