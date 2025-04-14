
class Places:
    def PlaceCenter(self, **kwargs):
        self.place(relx=0.5, rely=0.5, anchor="center", **kwargs)

    def PlaceTop(self, offset=0.1, **kwargs):
        self.place(relx=0.5, rely=offset, anchor="n", **kwargs)

    def PlaceBottom(self, offset=0.95, **kwargs):
        self.place(relx=0.5, rely=offset, anchor="s", **kwargs)

    def PlaceLeft(self, offset=0.1, **kwargs):
        self.place(relx=offset, rely=0.5, anchor="w", **kwargs)

    def PlaceRight(self, offset=0.9, **kwargs):
        self.place(relx=offset, rely=0.5, anchor="e", **kwargs)

    def PlaceTopLeft(self, x=0.05, y=0.05, **kwargs):
        self.place(relx=x, rely=y, anchor="nw", **kwargs)

    def PlaceBottomRight(self, x=0.95, y=0.95, **kwargs):
        self.place(relx=x, rely=y, anchor="se", **kwargs)
