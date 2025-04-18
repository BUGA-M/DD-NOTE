import customtkinter as ctk

class ChangeFrame:
    def __init__(self, root):
        self.root=root
        self.current_frame = None

    def show_frame(self,new_frame):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame=new_frame(self.root)
        self.current_frame.FramePlace()