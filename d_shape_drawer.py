import tkinter as tk
from tkinter import filedialog
import json

class ShapeDrawerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Shape Drawer")
        
        # Initialize variables for shape parameters
        self.shapes = []
        self.selected_shape = None
        
        # Create frame for controls
        control_frame = tk.Frame(master)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Shape type dropdown menu
        tk.Label(control_frame, text="Select Shape:").pack()
        shapes = ["Circle", "Rectangle", "Line"]
        self.shape_type = tk.StringVar()
        tk.OptionMenu(control_frame, self.shape_type, *shapes).pack()
        
        # Color selection
        tk.Label(control_frame, text="Select Color:").pack()
        self.color_entry = tk.Entry(control_frame)
        self.color_entry.pack()
        
        # Size input
        tk.Label(control_frame, text="Size:").pack()
        self.size_entry = tk.Entry(control_frame)
        self.size_entry.pack()
        
        # Buttons
        tk.Button(control_frame, text="Draw", command=self.draw_shape).pack()
        tk.Button(control_frame, text="Delete", command=self.delete_shape).pack()
        tk.Button(control_frame, text="Save", command=self.save_shapes).pack()
        tk.Button(control_frame, text="Load", command=self.load_shapes).pack()
        
        # Canvas for drawing shapes
        self.canvas = tk.Canvas(master, width=400, height=300, bg="white")
        self.canvas.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Binding mouse events to canvas
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # Variables to store mouse position
        self.start_x = None
        self.start_y = None
    
    def on_click(self, event):
        # Record starting position of mouse
        self.start_x = event.x
        self.start_y = event.y
        self.selected_shape = None
        
        # Check if the cursor is hovering over any existing shape
        for shape in self.shapes:
            if self.canvas.find_withtag("current") == shape['id']:
                self.selected_shape = shape
                break

    def on_drag(self, event):
        # Check if starting point exists
        if self.start_x is not None and self.start_y is not None:
            current_x = event.x
            current_y = event.y
            
            # Check if there's a shape to resize
            if self.selected_shape:
                shape_id = self.selected_shape['id']
                shape_type = self.selected_shape['type']
                color = self.selected_shape['color']
                size = self.selected_shape['size']
                
                # Draw shape based on starting and current points
                if shape_type == "Circle":
                    # Calculate the radius of the circle based on the distance between starting and current points
                    radius = ((current_x - self.start_x)**2 + (current_y - self.start_y)**2)**0.5
                    # Draw the circle centered at the starting point with the calculated radius
                    self.canvas.delete(shape_id)
                    self.canvas.create_oval(self.start_x - radius, self.start_y - radius, self.start_x + radius, self.start_y + radius, outline=color, tags="shape")
                elif shape_type == "Rectangle":
                    # Draw the rectangle using the starting point and the current point
                    self.canvas.delete(shape_id)
                    self.canvas.create_rectangle(self.start_x, self.start_y, current_x, current_y, outline=color, tags="shape")
                elif shape_type == "Line":
                    # Draw the line from the starting point to the current point
                    self.canvas.delete(shape_id)
                    self.canvas.create_line(self.start_x, self.start_y, current_x, current_y, fill=color, tags="shape")

    def on_release(self, event):
        # Reset mouse position
        self.start_x = None
        self.start_y = None
    
    def draw_shape(self):
        # Draw shape on button click
        self.clear_canvas()
        shape_type = self.shape_type.get()
        color = self.color_entry.get()
        size = int(self.size_entry.get())
        if shape_type == "Circle":
            shape_id = self.canvas.create_oval(200-size, 150-size, 200+size, 150+size, fill=color, outline=color)
        elif shape_type == "Rectangle":
            shape_id = self.canvas.create_rectangle(200-size, 150-size, 200+size, 150+size, fill=color, outline=color)
        elif shape_type == "Line":
            shape_id = self.canvas.create_line(200-size, 150, 200+size, 150, fill=color)
        self.shapes.append({'id': shape_id, 'type': shape_type, 'color': color, 'size': size})
    
    def delete_shape(self):
        # Delete selected shape
        if self.selected_shape:
            shape_id = self.selected_shape['id']
            self.canvas.delete(shape_id)
            self.shapes.remove(self.selected_shape)
            self.selected_shape = None
    
    def save_shapes(self):
        # Save shapes to file
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'w') as file:
                json.dump(self.shapes, file)
    
    def load_shapes(self):
        # Load shapes from file
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r') as file:
                self.shapes = json.load(file)
            self.clear_canvas()
            for shape in self.shapes:
                shape_type = shape['type']
                color = shape['color']
                size = shape['size']
                if shape_type == "Circle":
                    shape_id = self.canvas.create_oval(200-size, 150-size, 200+size, 150+size, fill=color, outline=color)
                elif shape_type == "Rectangle":
                    shape_id = self.canvas.create_rectangle(200-size, 150-size, 200+size, 150+size, fill=color, outline=color)
                elif shape_type == "Line":
                    shape_id = self.canvas.create_line(200-size, 150, 200+size, 150, fill=color)
                shape['id'] = shape_id
    
    def clear_canvas(self):
        # Clear canvas
        self.canvas.delete("all")
    
def main():
    root = tk.Tk()
    app = ShapeDrawerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
