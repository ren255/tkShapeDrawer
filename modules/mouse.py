class mouse:
    def __init__(self):
        pass
    
    def setpos(self, event):
        self.pos = (event.x, event.y)
        return self.pos
    
    def getpos(self,event):
        return (event.x,event.y)

    def getPpos(self):
        return self.pos

    def getdiff(self, event,reset=False):
        diffpos = (
            event.x - self.pos[0],
            event.y - self.pos[1],
        )
        if reset==True:
            self.setpos(event)
        return diffpos
    
    def getrec(self,event):
        rec = (
            *self.pos,
            *self.getdiff(event),
        )
        return rec